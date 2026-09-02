from sqlalchemy import Column, BigInteger, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class IMRecord(Base):
    __tablename__ = "im_record"

    id = Column(BigInteger, primary_key=True, index=True)  # record_id → id
    # swim_record(record_id)와 1:1 관계라 FK = PK
    record_id = Column(BigInteger, ForeignKey("swim_record.id"), unique=True)

    back_distance = Column(Integer, nullable=True)
    back_time = Column(Time, nullable=True)
    breast_distance = Column(Integer, nullable=True)
    breast_time = Column(Time, nullable=True)
    fly_distance = Column(Integer, nullable=True)
    fly_time = Column(Time, nullable=True)
    free_distance = Column(Integer, nullable=True)
    free_time = Column(Time, nullable=True)

    record = relationship("SwimRecord", back_populates="im_record")
