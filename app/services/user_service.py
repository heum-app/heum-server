from datetime import date

from sqlalchemy.orm import Session

from app.crud.user import (
    delete_user_related_db_data,
    update_user_info_by_id,
    update_user_profile_by_id,
    withdraw_user_by_id,
)
from app.models.user.user import User
from app.services.auth_service import social_unlink_service
from app.utils.s3 import delete_image_from_s3, upload_image_to_s3


def update_user_service(
    db: Session,
    user: User,
    gender: str | None = None,
    birth_date: date | None = None,
    is_public: bool | None = None,
):
    """회원 정보 수정 서비스 로직 (트랜잭션 관리)"""
    try:
        updated_user = update_user_info_by_id(
            db, user.id, gender, birth_date, is_public
        )
        db.commit()
        db.refresh(updated_user)
        return updated_user
    except Exception as e:
        db.rollback()
        raise e


def update_user_profile_service(
    db: Session, user: User, nickname: str | None, bio: str | None, profile_image: any
):
    """프로필 수정 서비스 로직 (S3 연동 및 트랜잭션 관리)"""
    new_image_url = None
    old_image_url = user.profile.profile_image_url if user.profile else None

    try:
        if profile_image:
            # 새 이미지 S3 업로드 (실패 시 Exception 발생하여 롤백됨)
            new_image_url = upload_image_to_s3(profile_image)

        # DB 업데이트
        update_user_profile_by_id(
            db, user.id, nickname=nickname, bio=bio, profile_image_url=new_image_url
        )

        db.commit()
        db.refresh(user)

        # DB 성공 후에만 기존 이미지 삭제
        if new_image_url and old_image_url:
            delete_image_from_s3(old_image_url)

        return user
    except Exception as e:
        db.rollback()
        # S3에 업로드는 성공했지만 DB가 실패한 경우, 방금 올린 파일 삭제
        if new_image_url:
            delete_image_from_s3(new_image_url)
        raise e


async def withdraw_user_service(db: Session, user: User):
    """
    회원 탈퇴 서비스 로직
    """
    profile_image_url = user.profile.profile_image_url if user.profile else None

    try:
        # 1. 소셜 연동 해제 (연동된 모든 계정 해제)
        await social_unlink_service(db, user.id)

        # 2. DB 작업
        delete_user_related_db_data(db, user.id)
        withdraw_user_by_id(db, user.id)

        db.commit()

        # 3. DB 성공 후 S3 실제 파일 삭제
        if profile_image_url:
            delete_image_from_s3(profile_image_url)

        return True
    except Exception as e:
        db.rollback()
        print(f"Withdraw Service Error: {e}")
        raise e
