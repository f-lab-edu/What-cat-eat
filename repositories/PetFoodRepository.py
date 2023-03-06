from repositories.RepositoryMeta import AbstractRepository
from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.pet_food import PetFood, Nutrient, Component
from schema.pet_food import PetFoodCreate, PetFoodGet, NutrientCreate, ComponentCreate
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

    def get_all_pet_food(self):
        return self.db.query(PetFood).all()

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

    def get_nutrient(self, id: int):
        nutrient = self.db.get(Nutrient, id)
        if not nutrient:
            return None
        return nutrient

    def get_nutrient_by_condition(self, condition):
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

    def update_nutrient(self, id: int, update_nutrient: NutrientCreate) -> Nutrient:
        update_nutrient.id = id
        self.db.merge(update_nutrient)
        self.db.commit()
        return update_nutrient

    def delete_nutrient(self, id: int) -> None:
        delete_user = self.db.get(Nutrient, id)
        self.db.delete(delete_user)
        self.db.commit()

    def get_component(self, id: int):
        component = self.db.get(Component, id)
        if not component:
            return None
        return component

    def get_component_by_condition(self, condition):
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

    def update_component(self, id: int, update_component: ComponentCreate) -> Nutrient:
        update_component.id = id
        self.db.merge(update_component)
        self.db.commit()
        return update_component

    def delete_component(self, id: int) -> None:
        delete_user = self.db.get(Component, id)
        self.db.delete(delete_user)
        self.db.commit()
