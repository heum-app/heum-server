from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class SocialAccount(Base):
    __tablename__ = "social_account"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    provider = Column(String(50), nullable=False)  # KAKAO / NAVER / GOOGLE
    social_id = Column(String(255), nullable=False)  # 각 provider의 고유 사용자 ID
    social_access_token = Column(Text, nullable=False)  # 각 provider의 고유 사용자 ID

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="social_accounts")