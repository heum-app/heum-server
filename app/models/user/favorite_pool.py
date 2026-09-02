from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class FavoritePool(Base):
    __tablename__ = "favorite_pools"

    id = Column(BigInteger, primary_key=True, index=True)  # user_pool_id → id
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    pool_id = Column(BigInteger, ForeignKey("pools.id"), nullable=False)

    user_pool_uuid = Column(String(36), nullable=True)
    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="favorite_pools")
    pool = relationship("Pool", back_populates="favorites")
