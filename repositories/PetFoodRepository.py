from repositories.RepositoryMeta import AbstractRepository
from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.pet_food import PetFood, Nutrient, Component
from schema.pet_food import (
    PetFoodCreate,
    PetFoodGet,
    NutrientGet,
    ComponentGet,
)
from sqlalchemy.orm import joinedload


class PetFoodRepository(AbstractRepository):
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: int) -> PetFood:
        pet_food = (
            self.db.query(PetFood)
            .options(joinedload(PetFood.nutrients), joinedload(PetFood.components))
            .filter(PetFood.id == id)
            .first()
        )

        if not pet_food:
            return None
        return pet_food

    def get_pet_food_by_name(self, name: str):
        pet_food = self.db.query(PetFood).filter(PetFood.name == name).first()
        if not pet_food:
            return None
        return pet_food

    def get_all_pet_foods(self):
        pet_foods = (
            self.db.query(PetFood)
            .options(joinedload(PetFood.nutrients), joinedload(PetFood.components))
            .all()
        )
        return pet_foods

    def create(self, pet_food: PetFoodCreate) -> PetFood:
        pet_food_obj = PetFood(name=pet_food.name)

        for nutrient in pet_food.nutrients:
            nutrient.pet_food_id = pet_food_obj.id

        for component in pet_food.components:
            component.pet_food_id = pet_food_obj.id

        pet_food_obj.nutrients = pet_food.nutrients
        pet_food_obj.components = pet_food.components

        self.db.add(pet_food_obj)
        self.db.commit()
        self.db.refresh(pet_food_obj)

        pet_food_get = PetFoodGet.from_orm(pet_food_obj)
        return pet_food_get

    def update(self, update_pet_food: PetFood) -> PetFood:
        self.db.commit()
        self.db.refresh(update_pet_food)
        return update_pet_food

    def delete(self, id: int) -> None:
        pet_food = self.db.get(PetFood, id)
        self.db.delete(pet_food)
        self.db.commit()

    def get_nutrient_by_condition(self, condition: NutrientGet):
        nutrient = (
            self.db.query(Nutrient)
            .filter(
                Nutrient.nutrient_name == condition.nutrient_name,
                Nutrient.percentage == condition.percentage,
                Nutrient.is_above == condition.is_above,
            )
            .first()
        )
        return nutrient

    def create_nutrient(self, nutrient: dict) -> Nutrient:
        nutrient_obj = Nutrient(
            nutrient_name=nutrient.nutrient_name,
            percentage=nutrient.percentage,
            is_above=nutrient.is_above,
        )

        self.db.add(nutrient_obj)
        self.db.commit()
        self.db.refresh(nutrient_obj)
        return nutrient_obj

    def get_component_by_condition(self, condition: ComponentGet):
        component = (
            self.db.query(Component)
            .filter(
                Component.component_name == condition.component_name,
            )
            .first()
        )
        return component

    def create_component(self, component: dict) -> Nutrient:
        component_obj = Component(
            component_name=component.component_name,
        )
        self.db.add(component_obj)
        self.db.commit()
        self.db.refresh(component_obj)
        return component_obj


class PetFoodFakeRepository(AbstractRepository):
    def __init__(self):
        self._pet_food = []
        self._nutirents = []
        self._components = []
        self._pet_food_nutrient = {}
        self._pet_food_component = {}

    def get(self, id) -> PetFood:
        if len(self._pet_food) < id:
            return None
        pet_food = self._pet_food[id - 1]
        return pet_food

    def get_pet_food_by_name(self, name: str):
        for pet_food in self._pet_food:
            if pet_food.name == name:
                return pet_food
        return None

    def get_all_pet_foods(self):
        return self._pet_food

    def create(self, pet_food: PetFood) -> PetFood:
        pet_food.id = len(self._pet_food) + 1
        self._pet_food.append(pet_food)

        nutrient_value = self._pet_food_nutrient.get(len(self._pet_food) - 1, [])
        component_value = self._pet_food_component.get(len(self._pet_food) - 1, [])

        for nutrient in pet_food.nutrients:
            nutrient_value.append(nutrient)

        for component in pet_food.components:
            component_value.append(component)

        self._pet_food_nutrient[len(self._pet_food) - 1] = nutrient_value
        self._pet_food_component[len(self._pet_food) - 1] = component_value
        return pet_food

    def update(self, update_pet_food: PetFood) -> PetFood:
        self._pet_food[update_pet_food.id - 1] = update_pet_food

        nutrient_value = self._pet_food_nutrient.get(len(self._pet_food) - 1, [])
        component_value = self._pet_food_component.get(len(self._pet_food) - 1, [])

        for nutrient in update_pet_food.nutrients:
            nutrient_value.append(nutrient)

        for component in update_pet_food.components:
            component_value.append(component)

        self._pet_food_nutrient[len(self._pet_food) - 1] = nutrient_value
        self._pet_food_component[len(self._pet_food) - 1] = component_value

        pet_food = self._pet_food[update_pet_food.id - 1]
        return pet_food

    def delete(self, id: int) -> None:
        del self._pet_food[id - 1]
        return len(self._pet_food)

    def get_nutrient_by_condition(self, condition: NutrientGet):
        if condition in self._nutirents:
            return condition
        return None

    def create_nutrient(self, nutrient: dict) -> Nutrient:
        self._nutirents.append(nutrient)
        return nutrient

    def get_component_by_condition(self, condition: NutrientGet):
        if condition in self._components:
            return condition
        return None

    def create_component(self, component: dict) -> Nutrient:
        self._nutirents.append(component)
        return component
