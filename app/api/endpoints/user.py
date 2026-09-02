from fastapi import APIRouter, Depends, status, File, UploadFile, Form, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user.user import User
from app.schemas.user import (
    UserResponse,
    UserUpdate,
)
from app.services.user_service import update_user_service, update_user_profile_service, withdraw_user_service
from datetime import datetime
from app.models.auth.auth_token import AuthToken

router = APIRouter()


@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    request_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """내 정보 수정"""
    return update_user_service(db, current_user, request_data.gender, request_data.birth_date, request_data.is_public)

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    """내 정보 조회"""
    return current_user

@router.put("/me/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_profile(
    nickname: str | None = Form(None),
    bio: str | None = Form(None),
    profile_image: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """내 프로필 (이미지, 닉네임, 소개) 수정"""
    return update_user_profile_service(
        db,
        current_user,
        nickname=nickname,
        bio=bio,
        profile_image=profile_image,
    )
    
@router.post("/me/withdraw")
async def withdraw_user(
    response: Response,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db), 
):
    """회원 탈퇴"""
    try:
        # 서비스 로직 호출 (소셜 언링크 및 DB 처리)
        await withdraw_user_service(db, current_user)
        
        # 쿠키 삭제
        response.delete_cookie("access_token", httponly=True)
        response.delete_cookie("refresh_token", httponly=True)
        
        return {"message": "계정이 성공적으로 삭제되었습니다."}
    except Exception as e:
        print(f"Withdraw Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail="탈퇴 처리 중 오류가 발생했습니다.")
