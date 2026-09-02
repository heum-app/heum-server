from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class WatchDevice(Base):
    __tablename__ = "watch_device"

    id = Column(BigInteger, primary_key=True, index=True)  # watch_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    device_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    connected_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="watch_devices")
