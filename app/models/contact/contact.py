from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(BigInteger, primary_key=True, index=True)  # contact_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    contact_uuid = Column(String(36), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    status = Column(
        String(20), nullable=False, default="PENDING"
    )  # ENUM 대신 문자열사용 (FastAPI/SQLAlchemy에서 더 유연함)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="contacts")
