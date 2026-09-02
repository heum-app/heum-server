from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(BigInteger, primary_key=True, index=True)

    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=False)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", backref="post_likes")
