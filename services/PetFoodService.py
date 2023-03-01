from repositories.PetFoodRepository import PetFoodRepository
from fastapi import Depends, HTTPException
from schema.pet_food import PetFoodCreateUpdate
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

    def get(self, id: int) -> PetFood:
        pet_food = self.pet_food_repository.get(id=id)
        if not pet_food:
            raise HTTPException(status_code=404, detail="해당 사료를 찾을 수 없습니다.")
        return pet_food

    def create(self, pet_food_body: PetFoodCreateUpdate) -> PetFood:
        return self.pet_food_repository.create(
            PetFood(
                **pet_food_body.dict(),
            )
        )

    def update(self, id: int, pet_food_body: PetFoodCreateUpdate) -> PetFood:
        return self.pet_food_repository.update(
            id,
            PetFood(
                **pet_food_body.dict(),
            ),
        )

    def delete(self, id: int) -> None:
        pet_food = self.get(id)

        if not pet_food:
            raise HTTPException(status_code=404, detail="해당 사료를 찾을 수 없습니다.")

        return self.pet_food_repository.delete(id)
