from typing import List
from pydantic import BaseModel


class NutrientBase(BaseModel):
    name: str
    percentage: int
    is_above: bool


class NutrientCreate(NutrientBase):
    pass


class Nutrient(NutrientBase):
    id: int
    pet_food_id: int

    class Config:
        orm_mode = True


class ComponentBase(BaseModel):
    name: str


class ComponentCreate(ComponentBase):
    pass


class Component(ComponentBase):
    id: int
    pet_food_id: int

    class Config:
        orm_mode = True


class PetFoodBase(BaseModel):
    name: str


class PetFoodGet(PetFoodBase):
    id: int
    nutrients: List[Nutrient] = []
    components: List[Component] = []

    class Config:
        orm_mode = True


class PetFoodCreateUpdate(PetFoodBase):
    nutrients: List[Nutrient] = []
    components: List[Component] = []
