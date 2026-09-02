from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Date,
    DateTime,
    Time,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class SwimRecord(Base):
    __tablename__ = "swim_record"

    id = Column(BigInteger, primary_key=True, index=True)  # record_id → id
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    record_uuid = Column(String(36), unique=True, nullable=False)
    swim_date = Column(Date, nullable=False)
    swim_distance = Column(Integer, nullable=False)
    swim_time = Column(Time, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    calories = Column(Integer, nullable=True)
    pool_length = Column(Integer, nullable=False)
    avrg_pace = Column(Time, nullable=True)
    avrg_heart_rate = Column(Integer, nullable=True)
    swim_pool = Column(String(255), nullable=True)
    etc_distance = Column(Integer, nullable=True)
    is_manual = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="swim_records")
    im_record = relationship("IMRecord", uselist=False, back_populates="record")
    heart_rates = relationship("SwimHeartRate", back_populates="record")
    diary = relationship("SwimDiary", uselist=False, back_populates="record")
