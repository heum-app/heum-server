from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(BigInteger, primary_key=True, index=True)
    condition = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("UserBadge", back_populates="badge")
