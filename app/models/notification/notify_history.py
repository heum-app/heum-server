from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class NotifyHistory(Base):
    __tablename__ = "notify_history"

    id = Column(BigInteger, primary_key=True, index=True)  # history_id → id

    notice_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    deeplink = Column(String(255), nullable=True)
    read_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="notify_histories")
