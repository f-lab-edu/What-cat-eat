from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Cat(Base):
    __tablename__ = "cat"

    id = Column(Integer, primary_key=True)
    represent_cat = Column(Boolean, nullable=False)
    name = Column(String(15), nullable=False)
    birth = Column(DateTime, nullable=False)
    img = Column(String(2083), nullable=True)
    gender = Column(String(6), nullable=False)
    species = Column(String(20), nullable=False)
    weight = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="cats")
