from sqlalchemy import Column, Integer, String, Text, DateTime

# 아까 database.py에서 받아온 Base
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(15), nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(15), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    
