from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.pet_food import PetFood, Nutrient, Component
from schema.pet_food import PetFoodCreateUpdate


class PetFoodRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: int) -> PetFood:
        pet_food = self.db.get(PetFood, id)
        if not pet_food:
            return None
        return pet_food

    def create(self, pet_food: PetFoodCreateUpdate) -> PetFood:
        nutrients = self.finding_nutrient(pet_food.nutrients)
        components = self.finding_components(pet_food.components)

        pet_food_obj = PetFood(name=pet_food.name)
        pet_food_obj.nutrient = nutrients
        pet_food_obj.component = components

        self.db.add(pet_food_obj)
        self.db.commit()
        self.db.refresh(pet_food_obj)
        return pet_food_obj

    def update(self, id: int, update_pet_food: PetFoodCreateUpdate) -> PetFood:
        pet_food = self.get(id)
        nutrients = self.finding_nutrient(pet_food.nutrients)
        components = self.finding_components(pet_food.components)

        if not pet_food:
            return None

        pet_food.name = update_pet_food.name
        pet_food.nutrient = nutrients
        pet_food.component = components

        self.db.commit()
        self.db.refresh(pet_food)
        return pet_food

    def delete(self, id: int) -> None:
        pet_food = self.db.get(PetFood, id)
        self.db.delete(pet_food)
        self.db.commit()

    def finding_nutrient(self, pet_food_nutrients) -> list:
        nutrients = []

        for nutrient in pet_food_nutrients:
            nutrient_obj = (
                self.db.query(Nutrient)
                .filter(
                    Nutrient.nutrient_name == nutrient["nutrient_name"],
                    Nutrient.percentage == nutrient["percentage"],
                    Nutrient.is_over == nutrient["is_over"],
                )
                .first()
            )

            if not nutrient_obj:
                nutrient_obj = self.create_nutrient(nutrient)
            nutrients.append(nutrient_obj)

        return nutrients

    def finding_components(self, pet_food_components) -> list:
        components = []

        for component in pet_food_components:
            component_obj = (
                self.db.query(Component)
                .filter(
                    Component.component_name == component["component_name"],
                )
                .first()
            )

            if not component_obj:
                component_obj = self.create_component(component)
            components.append(component_obj)

        return components

    def create_nutrient(self, nutrient: dict) -> Nutrient:
        nutrient_obj = Nutrient(
            nutrient_name=nutrient["nutrient_name"],
            percentage=nutrient["percentage"],
            is_over=nutrient["is_over"],
        )

        self.db.add(nutrient_obj)
        self.db.commit()
        self.db.refresh(nutrient_obj)
        return nutrient_obj

    def create_component(self, component: dict) -> Component:
        component_obj = Component(component_name=component["component_name"])

        self.db.add(component_obj)
        self.db.commit()
        self.db.refresh(component_obj)
        return component_obj
