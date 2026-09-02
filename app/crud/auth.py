from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.auth.auth_token import AuthToken
from app.models.auth.social_account import SocialAccount


def get_social_account(db: Session, provider: str, social_id: str):
    """소셜 계정 조회"""
    return (
        db.query(SocialAccount)
        .filter(
            SocialAccount.provider == provider, SocialAccount.social_id == social_id
        )
        .first()
    )


def get_social_accounts_by_user_id(db: Session, user_id: int):
    """유저의 모든 소셜 계정 리스트 조회"""
    return db.query(SocialAccount).filter(SocialAccount.user_id == user_id).all()


def get_social_account_by_user_id(db: Session, user_id: int):
    """소셜 계정 단건 조회"""
    return db.query(SocialAccount).filter(SocialAccount.user_id == user_id).first()


def get_social_account_by_social_id(db: Session, social_id: str):
    """소셜 계정 조회"""
    return db.query(SocialAccount).filter(SocialAccount.social_id == social_id).first()


def create_social_account(
    db: Session, user_id: int, provider: str, social_id: str, social_access_token: str
):
    """소셜 계정 생성"""
    new_acc = SocialAccount(
        user_id=user_id,
        provider=provider,
        social_id=social_id,
        social_access_token=social_access_token,
    )
    db.add(new_acc)
    db.flush()

    return new_acc


def update_user_social_token(
    db: Session, social_account: SocialAccount, new_token: str
):
    """소셜 액세스 토큰 최신화"""
    social_account.social_access_token = new_token
    db.flush()
    return social_account


def update_user_refresh_token(
    db: Session, user_id: int, refresh_token: str, device: str = "web"
):
    """유저의 리프레시 토큰을 DB에 저장하거나 업데이트"""
    token_record = (
        db.query(AuthToken)
        .filter(AuthToken.user_id == user_id, AuthToken.device_type == device)
        .first()
    )

    if token_record:
        token_record.refresh_token = refresh_token
        token_record.is_valid = True
        token_record.created_at = datetime.utcnow()
        # 만료 시간 설정 (예: 7일)
        token_record.expired_at = datetime.utcnow() + timedelta(days=7)
    else:
        # 존재하지 않으면 새 레코드 생성
        token_record = AuthToken(
            user_id=user_id,
            refresh_token=refresh_token,
            device_type=device,
            is_valid=True,
            created_at=datetime.utcnow(),
            expired_at=datetime.utcnow() + timedelta(days=7),
        )
        db.add(token_record)

    try:
        db.flush()
        return token_record
    except Exception as e:
        raise e


def verify_user_refresh_token(
    db: Session, user_id: int, refresh_token: str, device: str = "web"
):
    """유저의 리프레시 토큰이 유효한지 DB에서 검증"""
    return (
        db.query(AuthToken)
        .filter(
            AuthToken.user_id == user_id,
            AuthToken.refresh_token == refresh_token,
            AuthToken.device_type == device,
            AuthToken.is_valid,
        )
        .first()
    )


def invalidate_user_refresh_token(db: Session, user_id: int, device: str = "web"):
    """유저의 리프레시 토큰 무효화"""
    token_record = (
        db.query(AuthToken)
        .filter(AuthToken.user_id == user_id, AuthToken.device_type == device)
        .first()
    )

    if token_record:
        token_record.is_valid = False
        db.flush()

    return True
