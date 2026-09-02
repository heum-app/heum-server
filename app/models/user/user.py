from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)  # user_id → id
    user_uuid = Column(String(36), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    is_public = Column(Boolean, nullable=False, default=True)
    phone_number = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # relationships
    profile = relationship("Profile", uselist=False, back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    swim_records = relationship("SwimRecord", back_populates="user")
    notifications_received = relationship(
        "Notification",
        foreign_keys="Notification.recipient_id",
        back_populates="recipient",
    )
    notifications_sent = relationship(
        "Notification", foreign_keys="Notification.sender_id", back_populates="sender"
    )
    followings = relationship(
        "UserFollow",
        foreign_keys="UserFollow.user_id",
        back_populates="user",
    )
    followers = relationship(
        "UserFollow", foreign_keys="UserFollow.following_id", back_populates="following"
    )
    social_accounts = relationship(
        "SocialAccount", back_populates="user", cascade="all, delete-orphan"
    )
