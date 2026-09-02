from sqlalchemy import Column, BigInteger, String
from app.db.base import Base


class NotifyTemplate(Base):
    __tablename__ = "notify_template"

    id = Column(BigInteger, primary_key=True, index=True)  # template_id → id

    key = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    deeplink = Column(String(255), nullable=True)
