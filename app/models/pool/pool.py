from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Pool(Base):
    __tablename__ = "pools"

    id = Column(BigInteger, primary_key=True, index=True)  # pool_id → id

    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)
    phone = Column(String(20), nullable=True)
    opening_time = Column(String(20), nullable=True)
    closing_time = Column(String(20), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    favorites = relationship("FavoritePool", back_populates="pool")
