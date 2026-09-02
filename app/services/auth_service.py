import os

import httpx
from fastapi import HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.crud.auth import (
    create_social_account,
    get_social_account,
    get_social_accounts_by_user_id,
    update_user_refresh_token,
    update_user_social_token,
    verify_user_refresh_token,
)
from app.crud.user import (
    create_user,
    create_user_profile,
    get_user_by_email,
    reactivate_user,
)
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserResponse
from app.utils.jwt_handeler import (
    create_access_token,
    create_refresh_token,
    verify_token,
)

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_URL = "https://kapi.kakao.com/v2/user/me"


async def social_login_service(request: LoginRequest, db: Session):
    provider = request.provider.upper()
    token = request.social_token

    # 1) 소셜 정보 조회
    if provider == "KAKAO":
        social_user = await get_kakao_user(token)
    elif provider == "NAVER":
        social_user = await get_naver_user(token)
    elif provider == "GOOGLE":
        social_user = await get_google_user(token)
    else:
        raise HTTPException(400, "지원하지 않는 provider 입니다.")

    social_id = social_user["id"]
    email = social_user.get("email")
    nickname = social_user.get("nickname", "사용자")
    profile_image_url = social_user.get("profile_image_url")

    try:
        # 2) 소셜 계정 존재 여부 확인
        social_account = get_social_account(db, provider, social_id)

        if social_account:
            user = social_account.user
            # 탈퇴 유저라면 복구
            if user.is_deleted:
                reactivate_user(db, user.id, email)
                # 탈퇴 시 프로필이 지워졌다면 새로 생성
                if not user.profile:
                    create_user_profile(db, user.id, nickname, profile_image_url)

            # 소셜 토큰 최신화
            update_user_social_token(db, social_account, token)
        else:
            # 3) 소셜 계정은 없지만 같은 이메일 유저가 있는지 확인
            user = get_user_by_email(db, email)

            # 마스킹 정책으로 인해 탈퇴 유저는 이메일로 검색되지 않음 (신규 가입 처리)
            if not user:
                user = create_user(
                    db,
                    UserCreate(
                        email=email,
                        nickname=nickname,
                        profile_image_url=profile_image_url,
                    ),
                )

            # 소셜 연동 추가
            create_social_account(db, user.id, provider, social_id, token)

        # 4) JWT 발급 및 DB 저장
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        update_user_refresh_token(db, user.id, refresh_token)

        db.commit()
        db.refresh(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": UserResponse.model_validate(user),
        }

    except Exception as e:
        db.rollback()
        raise e


async def get_kakao_user(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://kapi.kakao.com/v2/user/me", headers=headers)

    if res.status_code != 200:
        raise HTTPException(400, "카카오 사용자 정보 조회 실패")

    data = res.json()

    return {
        "id": str(data["id"]),
        "email": data.get("kakao_account", {}).get("email"),
        "nickname": data.get("kakao_account", {}).get("profile", {}).get("nickname"),
        "profile_image_url": data.get("kakao_account", {})
        .get("profile", {})
        .get("profile_image_url"),
    }


async def get_naver_user(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://openapi.naver.com/v1/nid/me", headers=headers)

    if res.status_code != 200:
        raise HTTPException(400, "네이버 사용자 정보 조회 실패")

    data = res.json()["response"]

    return {
        "id": data["id"],
        "email": data.get("email"),
        "nickname": data.get("name"),
        "profile_image_url": data.get("profile_image"),
        # gender, birthday
    }


async def get_google_user(id_token_str: str):
    """Google ID Token(JWT)을 검증·디코딩하여 사용자 정보를 반환"""
    try:
        data = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
        )
    except ValueError:
        raise HTTPException(400, "구글 사용자 정보 조회 실패")

    return {
        "id": data["sub"],
        "email": data.get("email"),
        "nickname": data.get("name"),
        "profile_image_url": data.get("picture"),
    }


async def unlink_kakao_user(access_token: str):
    """
    카카오 소셜 연결 끊기
    """
    url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers)

    if res.status_code != 200:
        return False

    return True


async def unlink_naver_user(access_token: str):
    """네이버 소셜 연결 끊기"""
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    url = "https://nid.naver.com/oauth2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        "grant_type": "delete",
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token,
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, params=params)

    if res.status_code != 200:
        return False

    return print(res.json())


async def unlink_google_user(access_token: str):
    """구글 소셜 연결 끊기"""
    url = "https://oauth2.googleapis.com/revoke"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {"token": access_token}

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, params=params)

    if res.status_code != 200:
        return False

    return True


async def social_unlink_service(db: Session, user_id: int):
    """
    유저의 모든 소셜 연동 해제 서비스
    """
    social_accounts = get_social_accounts_by_user_id(db, user_id)
    if not social_accounts:
        return

    for social_account in social_accounts:
        provider = social_account.provider.upper()
        try:
            if provider == "KAKAO":
                await unlink_kakao_user(social_account.social_access_token)
            elif provider == "NAVER":
                await unlink_naver_user(social_account.social_access_token)
            elif provider == "GOOGLE":
                await unlink_google_user(social_account.social_access_token)
        except Exception as e:
            print(f"Social Unlink Failure ({provider}): {e}")


def refresh_token_service(refresh_token: str, db: Session):
    """리프레시 토큰 검증 후 새로운 엑세스 토큰 발급"""
    payload = verify_token(refresh_token)

    # 리프레시 토큰이 유효하지 않거나 만료된 경우
    if not payload or "error" in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 유효하지 않거나 만료되었습니다. 다시 로그인해 주세요.",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 잘못된 데이터가 포함되어 있습니다.",
        )

    # 1. DB 검증
    is_valid_db_token = verify_user_refresh_token(db, user_id, refresh_token)
    if not is_valid_db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이전에 로그아웃했거나 유효하지 않은 임의의 토큰입니다. 다시 로그인 해주세요.",
        )

    # access, refresh 토큰 생성
    access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token({"sub": str(user_id)})

    # 2. 갱신된 리프레시 토큰을 DB에 저장
    try:
        update_user_refresh_token(db, user_id, new_refresh_token)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
