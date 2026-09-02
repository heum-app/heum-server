from datetime import datetime
from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class NotificationSetting(Base):
    __tablename__ = "notification_settings"

    id = Column(BigInteger, primary_key=True, index=True)  # setting_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    follow_alert = Column(Boolean, default=True)
    comment_alert = Column(Boolean, default=True)
    like_alert = Column(Boolean, default=True)
    ranking_alert = Column(Boolean, default=True)
    goal_alert = Column(Boolean, default=True)
    badge_alert = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="notification_settings")
