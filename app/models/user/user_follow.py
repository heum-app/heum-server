from datetime import datetime
from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserFollow(Base):
    __tablename__ = "user_follows"

    id = Column(BigInteger, primary_key=True, index=True)  # user_follow_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    following_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(BigInteger, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="followings")
    following = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )
