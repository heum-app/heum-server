from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date

# 공통 스키마
class UserBase(BaseModel):
    email: str
    name: str


# 회원가입 (Request)
class UserCreate(BaseModel):
    email: EmailStr
    nickname: str
    profile_image_url: str


# 회원 정보 수정 (Request)
class UserUpdate(BaseModel):
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    is_public: Optional[bool] = None


# 회원 프로필 조회 (Response)
class ProfileResponse(BaseModel):
    id: int
    nickname: str | None
    profile_image_url: str | None
    bio: str | None

    model_config = ConfigDict(from_attributes=True)


# 회원 정보 조회 (Response)
class UserResponse(BaseModel):
    id: int
    email: str
    birth_date: date | None
    gender: str | None
    profile: ProfileResponse | None

    model_config = ConfigDict(from_attributes=True)
