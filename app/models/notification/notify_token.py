from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class NotifyToken(Base):
    __tablename__ = "notify_token"

    id = Column(BigInteger, primary_key=True, index=True)  # token_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    device_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    token = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="notify_tokens")
