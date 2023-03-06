from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Table,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

pet_food_nutrient = Table(
    "pet_food_nutrient",
    Base.metadata,
    Column("pet_food_id", Integer, ForeignKey("pet_food.id"), primary_key=True),
    Column("nutrient_id", Integer, ForeignKey("nutrient.id"), primary_key=True),
)


pet_food_component = Table(
    "pet_food_component",
    Base.metadata,
    Column("pet_food_id", Integer, ForeignKey("pet_food.id"), primary_key=True),
    Column("component_id", Integer, ForeignKey("component.id"), primary_key=True),
)


class Nutrient(Base):
    __tablename__ = "nutrient"

    id = Column(Integer, primary_key=True)
    nutrient_name = Column(String(30), nullable=False)
    percentage = Column(Integer, nullable=False)
    is_above = Column(Boolean, nullable=False)

    pet_food = relationship(
        "PetFood", secondary=pet_food_nutrient, back_populates="nutrients"
    )

    __table_args__ = (UniqueConstraint("nutrient_name", "percentage", "is_above"),)


class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True)
    component_name = Column(String(10), nullable=False)

    pet_food = relationship(
        "PetFood", secondary=pet_food_component, back_populates="components"
    )

    __table_args__ = (UniqueConstraint("component_name"),)


class PetFood(Base):
    __tablename__ = "pet_food"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    nutrients = relationship(
        "Nutrient", secondary=pet_food_nutrient, back_populates="pet_food"
    )
    components = relationship(
        "Component", secondary=pet_food_component, back_populates="pet_food"
    )
