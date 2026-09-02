from datetime import datetime
from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class SwimDiary(Base):
    __tablename__ = "swim_diary"

    id = Column(BigInteger, primary_key=True, index=True)  # record_id → id

    record_id = Column(BigInteger, ForeignKey("swim_record.id"))
    user_id = Column(BigInteger, ForeignKey("users.id"))

    content = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    record = relationship("SwimRecord", back_populates="diary")
    user = relationship("User", backref="diaries")
