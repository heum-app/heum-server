import uuid
from sqlalchemy.orm import Session
from app.models.user.profile import Profile
from app.models.user.user import User
from app.models.auth.social_account import SocialAccount
from app.models.auth.auth_token import AuthToken
from app.schemas.user import UserCreate
from sqlalchemy.orm import joinedload
from datetime import date, datetime


def get_user_by_email(db: Session, email: str):
    """이메일 조회 쿼리"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_uid(db: Session, uid: str):
    """uid 조회 쿼리"""
    return db.query(User).filter(User.uid == uid).first()


def create_user(db: Session, data: UserCreate):
    """회원 등록 쿼리"""
    new_user = User(
        email=data.email,
        user_uuid=str(uuid.uuid4()),
    )
    db.add(new_user)
    db.flush()  # ID 확보를 위해 flush
    
    # 프로필 생성
    create_user_profile(db, new_user.id, data.nickname, data.profile_image_url)
    
    return new_user

def create_user_profile(db: Session, user_id: int, nickname: str | None = None, profile_image_url: str | None = None):
    """회원 프로필 생성 쿼리"""
    profile = Profile(
        user_id=user_id,
        nickname=nickname,
        profile_image_url=profile_image_url,
    )
    db.add(profile)
    db.flush()

    return profile


def update_user_info_by_id(db: Session, user_id: int, gender: str | None = None, birth_date: date | None = None, is_public: bool | None = None):
    """회원 정보 수정 쿼리"""
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        if gender is not None:
            user.gender = gender
        if birth_date is not None:
            user.birth_date = birth_date
        if is_public is not None:
            user.is_public = is_public
        db.flush()

    return user


def update_user_profile_by_id(
    db: Session,
    user_id: int,
    nickname: str | None = None,
    bio: str | None = None,
    profile_image_url: str | None = None,
):
    """회원 프로필 수정 쿼리"""
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        if nickname is not None:
            profile.nickname = nickname
        if bio is not None:
            profile.bio = bio
        if profile_image_url is not None:
            profile.profile_image_url = profile_image_url
            
        db.flush()
        
    return profile


def delete_user_related_db_data(db: Session, user_id: int):
    """탈퇴 시 연관 데이터 삭제 (Profile, Token 삭제)"""
    db.query(Profile).filter(Profile.user_id == user_id).delete()
    db.query(AuthToken).filter(AuthToken.user_id == user_id).delete()
    # SocialAccount는 복구를 위해 삭제하지 않고 유지

def withdraw_user_by_id(db: Session, user_id: int):
    """회원 탈퇴 쿼리 (Masking 적용)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # 이메일 마스킹
        if not user.email.startswith("deleted_"):
            user.email = f"deleted_{user.id}_{user.email}"
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()
        db.flush()
    return user

def reactivate_user(db: Session, user_id: int, original_email: str):
    """회원 탈퇴 복구 쿼리"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = original_email
        user.is_deleted = False
        user.deleted_at = None
        db.flush()
    return user
