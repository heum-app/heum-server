# app/api/routers.py
from fastapi import APIRouter
from app.api.endpoints import auth, user

api_router = APIRouter()

# 각각의 endpoint 라우터를 등록
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
