from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import (
    refresh_token_service,
    social_login_service,
)
from app.crud.auth import invalidate_user_refresh_token
from app.dependencies import get_current_user
from app.models.user.user import User
from app.utils.jwt_handeler import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def social_login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    회원 로그인 API
    """
    result = await social_login_service(request, db)


    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,     # js로 접근 불가
        secure=False,       # https 통신일 때만 쿠키 전송
        samesite="lax",    # CSRF 방어
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    
    return LoginResponse(message="로그인 성공", user=result["user"])


@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    access, refresh 토큰 재발급 API
    """
    refresh_token_cookie = request.cookies.get("refresh_token")
    if not refresh_token_cookie:
        raise HTTPException(status_code=401, detail="Refresh token missing")
        
    result = refresh_token_service(refresh_token_cookie, db=db)
    
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 30분
    )
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 7일
    )
    
    return {"message": "토큰이 성공적으로 재발급되었습니다."}


@router.post("/logout")
def logout(response: Response, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    로그아웃 API
    """
    # 브라우저 쿠키 삭제
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    # DB 토큰 무효화
    invalidate_user_refresh_token(db, current_user.id)
    
    return {"message": "로그아웃 되었습니다."}
