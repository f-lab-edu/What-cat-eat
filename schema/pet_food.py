from typing import List, Optional
from pydantic import BaseModel, Field


class NutrientBase(BaseModel):
    nutrient_name: str
    percentage: int
    is_above: bool


class NutrientCreate(NutrientBase):
    pass


class NutrientGet(NutrientBase):
    id: Optional[int]
    pet_food_id: Optional[int] = None

    class Config:
        orm_mode = True


class ComponentBase(BaseModel):
    component_name: str


class ComponentCreate(ComponentBase):
    pass


class ComponentGet(ComponentBase):
    id: Optional[int]
    pet_food_id: Optional[int] = None

    class Config:
        orm_mode = True


class PetFoodBase(BaseModel):
    name: str
    nutrients: List[NutrientGet] = []
    components: List[ComponentGet] = []


class PetFoodGet(PetFoodBase):
    id: Optional[int] = Field(primary_key=True)

    class Config:
        orm_mode = True


class PetFoodCreate(PetFoodBase):
    pet_food_id: int = None


class PetFoodUpdate(PetFoodBase):
    id: Optional[int] = Field(primary_key=True)
    pet_food_id: int = None
