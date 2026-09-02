from datetime import datetime
from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class PostPreference(Base):
    __tablename__ = "post_preferences"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)

    is_hidden = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(BigInteger, nullable=False)

    user = relationship("User", backref="post_preferences")
    post = relationship("Post", back_populates="preferences")
