from repositories.PetFoodRepository import PetFoodRepository
from fastapi import Depends, HTTPException
from schema.pet_food import PetFoodCreate, PetFoodUpdate, PetFoodGet
from models.pet_food import PetFood
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PetFoodService:
    pet_food_repository: PetFoodRepository

    def __init__(
        self,
        pet_food_repository: PetFoodRepository = Depends(),
    ) -> None:
        self.pet_food_repository = pet_food_repository

    def get(self, id: int) -> PetFoodGet:
        pet_food = self.pet_food_repository.get(id=id)
        if not pet_food:
            raise HTTPException(status_code=404, detail="해당 사료를 찾을 수 없습니다.")
        return pet_food

    def get_all_pet_foods(self):
        pet_foods = self.pet_food_repository.get_all_pet_foods()
        return pet_foods

    def create(self, pet_food_body: PetFoodCreate) -> PetFood:
        find_pet_food_by_name = self.pet_food_repository.get_pet_food_by_name(
            pet_food_body.name
        )
        if find_pet_food_by_name:
            raise HTTPException(status_code=409, detail="해당 사료는 이미 존재합니다.")

        nutrients = self.finding_nutrient(pet_food_body.nutrients)
        components = self.finding_components(pet_food_body.components)

        return self.pet_food_repository.create(
            PetFood(name=pet_food_body.name, nutrients=nutrients, components=components)
        )

    def update(self, id: int, pet_food_body: PetFoodUpdate) -> PetFood:
        pet_food = self.get(id)

        if pet_food_body.nutrients:
            nutrients = self.finding_nutrient(pet_food_body.nutrients)
        else:
            nutrients = pet_food.nutrients

        if pet_food_body.components:
            components = self.finding_components(pet_food_body.components)
        else:
            components = pet_food.components

        pet_food.name = pet_food_body.name
        pet_food.nutrients = nutrients
        pet_food.components = components

        return self.pet_food_repository.update(update_pet_food=pet_food)

    def delete(self, id: int) -> None:
        self.get(id)
        return self.pet_food_repository.delete(id)

    def finding_nutrient(self, pet_food_nutrients: list) -> list:
        nutrients = []

        for nutrient in pet_food_nutrients:
            nutrient_obj = self.pet_food_repository.get_nutrient_by_condition(nutrient)
            if not nutrient_obj:
                nutrient_obj = self.pet_food_repository.create_nutrient(nutrient)

            if nutrient_obj not in nutrients:
                nutrients.append(nutrient_obj)

        return nutrients

    def finding_components(self, pet_food_components: list) -> list:
        components = []

        for component in pet_food_components:
            component_obj = self.pet_food_repository.get_component_by_condition(
                component
            )
            if not component_obj:
                component_obj = self.pet_food_repository.create_component(component)

            if component_obj not in components:
                components.append(component_obj)

        return components
