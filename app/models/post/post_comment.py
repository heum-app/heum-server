from datetime import datetime
from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(BigInteger, primary_key=True, index=True)

    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(BigInteger, nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", backref="post_comments")
