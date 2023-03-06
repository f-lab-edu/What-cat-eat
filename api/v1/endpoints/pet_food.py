from fastapi import APIRouter, Depends, status
from services.PetFoodService import PetFoodService
from schema.pet_food import PetFoodGet, PetFoodCreate, PetFoodUpdate

router = APIRouter(
    prefix="/petfood",
)


@router.get("/{id}", response_model=PetFoodGet, status_code=status.HTTP_200_OK)
def get_pet_food(id: int, pet_food_service: PetFoodService = Depends()):
    return pet_food_service.get(id)


@router.post("", response_model=PetFoodGet, status_code=status.HTTP_201_CREATED)
def create_pet_food(
    pet_food_body: PetFoodCreate,
    pet_food_service: PetFoodService = Depends(),
):

    return pet_food_service.create(pet_food_body)


@router.put("/{id}", response_model=PetFoodGet, status_code=status.HTTP_200_OK)
def update_pet_food(
    id: int,
    pet_food_body: PetFoodUpdate,
    pet_food_service: PetFoodService = Depends(),
):
    return pet_food_service.update(id, pet_food_body)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_pet_food(
    id: int,
    pet_food_service: PetFoodService = Depends(),
):
    pet_food_service.delete(id)
    return {"detail": "삭제되었습니다."}
