from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Date,
    Boolean,
    DECIMAL,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(BigInteger, primary_key=True, index=True)  # goal_id → id
    goal_uuid = Column(String(36), unique=True, nullable=False)

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    goal_type = Column(String(50), nullable=False)
    current_value = Column(DECIMAL(10, 2), default=0)
    target_value = Column(DECIMAL(10, 2), nullable=False)
    is_achieved = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="goals")
