from sqlalchemy import Column, Integer, String, DateTime

from database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(15), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(15), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
