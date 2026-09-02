from typing import Literal, Optional
from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


# 로그인 (Request)
class LoginRequest(BaseModel):
    provider: str
    social_token: str


# 로그인 성공 (Response)
class LoginResponse(BaseModel):
    message: str
    user: UserResponse
