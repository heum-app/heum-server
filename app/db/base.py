from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# 모델 연결
from app.models import *
