from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(BigInteger, primary_key=True, index=True)  # token_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    refresh_token = Column(String(255), nullable=False)
    device_type = Column(String(50), nullable=False)
    is_valid = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime, nullable=False)

    user = relationship("User", backref="auth_tokens")
