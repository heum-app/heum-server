from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Notification(Base):
    __tablename__ = "notification"

    id = Column(BigInteger, primary_key=True, index=True)  # notification_id → id
    notification_uuid = Column(String(36), unique=True, nullable=False)

    recipient_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    sender_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    type = Column(
        Enum(
            "FOLLOW",
            "LIKE",
            "COMMENT",
            "WAKEUP",
            "GOAL",
            "BADGE",
            name="notification_type",
        ),
        nullable=False,
    )

    content = Column(Text, nullable=False)
    target_id = Column(BigInteger, nullable=True)
    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    recipient = relationship(
        "User", foreign_keys=[recipient_id], back_populates="notifications_received"
    )
    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="notifications_sent"
    )
