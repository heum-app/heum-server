from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class SwimHeartRate(Base):
    __tablename__ = "swim_heart_rate"

    id = Column(BigInteger, primary_key=True, index=True)
    record_id = Column(BigInteger, ForeignKey("swim_record.id"), nullable=False)
    measured_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    bpm = Column(Integer, nullable=False)

    record = relationship("SwimRecord", back_populates="heart_rates")
