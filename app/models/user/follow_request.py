from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class FollowRequest(Base):
    __tablename__ = "follow_requests"

    id = Column(BigInteger, primary_key=True, index=True)

    requester_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    target_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    status = Column(
        Enum("0", "1", "2", name="follow_request_status"), default="0", nullable=False
    )  # 0=요청, 1=수락, 2=거절

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requester = relationship(
        "User", foreign_keys=[requester_id], backref="sent_follow_requests"
    )
    target = relationship(
        "User", foreign_keys=[target_id], backref="received_follow_requests"
    )
