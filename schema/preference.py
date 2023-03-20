from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AllergyBase(BaseModel):
    allergy_name: str


class AllergyCreate(AllergyBase):
    pass


class AllergyGet(AllergyBase):
    id: Optional[int]
    cat_id: Optional[int] = None

    class Config:
        orm_mode = True


class PetFoodPreferenceBase(BaseModel):
    preference: str
    memo: Optional[str] = None
    allergies: List[AllergyGet] = []


class PetFoodPreferenceGet(PetFoodPreferenceBase):
    id: Optional[int] = Field(primary_key=True)
    created_at: datetime
    updated_at: datetime
    pet_food_id: int
    cat_id: int

    class Config:
        orm_mode = True


class PetFoodPreferenceCreate(PetFoodPreferenceBase):
    pet_food_id: int
    cat_id: int


class PetFoodPreferenceUpdate(PetFoodPreferenceBase):
    id: Optional[int] = Field(primary_key=True)
    pet_food_id: int
    cat_id: int
