from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


pet_food_preference_allergy = Table(
    "pet_food_preference_allergy",
    Base.metadata,
    Column(
        "pet_food_preference_id",
        Integer,
        ForeignKey("pet_food_preference.id"),
        primary_key=True,
    ),
    Column("allergy_id", Integer, ForeignKey("allergy.id"), primary_key=True),
)


class Allergy(Base):
    __tablename__ = "allergy"

    id = Column(Integer, primary_key=True)
    allergy_name = Column(String(20), nullable=False)

    pet_food_preference = relationship(
        "PetFoodPreference",
        secondary=pet_food_preference_allergy,
        back_populates="allergies",
    )


class PetFoodPreference(Base):
    __tablename__ = "pet_food_preference"

    id = Column(Integer, primary_key=True)
    preference = Column(String(10), nullable=False)
    memo = Column(String(500), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    allergies = relationship(
        "Allergy",
        secondary=pet_food_preference_allergy,
        back_populates="pet_food_preference",
    )

    pet_food_id = Column(Integer, ForeignKey("pet_food.id", ondelete="CASCADE"))
    pet_food = relationship("PetFood", back_populates="preference")

    cat_id = Column(Integer, ForeignKey("cat.id", ondelete="CASCADE"))
    cat = relationship("Cat", back_populates="preferences")
