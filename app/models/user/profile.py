from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(BigInteger, primary_key=True, index=True)  # user_profile_id → id
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    nickname = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(Text, nullable=True)
    post_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(BigInteger, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="profile")
