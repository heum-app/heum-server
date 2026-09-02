from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    badge_id = Column(BigInteger, ForeignKey("badges.id"), nullable=False)

    acquired_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="users")
