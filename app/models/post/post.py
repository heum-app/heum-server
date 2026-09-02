from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    String,
    JSON,
    Enum,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, index=True)  # post_id → id

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=True)
    hash_tags = Column(JSON, nullable=True)
    image_urls = Column(JSON, nullable=True)

    visibility = Column(
        Enum("friends", "private", name="post_visibility"),
        default="friends",
        nullable=False,
    )

    is_updated = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(BigInteger, nullable=False)

    user = relationship("User", backref="posts")
    likes = relationship(
        "PostLike", back_populates="post", cascade="all, delete-orphan"
    )
    comments = relationship(
        "PostComment", back_populates="post", cascade="all, delete-orphan"
    )
    preferences = relationship(
        "PostPreference", back_populates="post", cascade="all, delete-orphan"
    )
