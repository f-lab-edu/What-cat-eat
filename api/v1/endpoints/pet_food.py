from fastapi import APIRouter, Depends, status
from services.PetFoodService import PetFoodService
from schema.pet_food import PetFoodGet, PetFoodCreateUpdate

router = APIRouter(
    prefix="/petfood",
)


@router.get("/{id}", response_model=PetFoodGet, status_code=status.HTTP_200_OK)
def get_pet_food(id: int, pet_food_service: PetFoodService = Depends()):
    return pet_food_service.get(id)


@router.post("", response_model=PetFoodGet, status_code=status.HTTP_201_CREATED)
def create_cat(
    pet_food_body: PetFoodCreateUpdate,
    pet_food_service: PetFoodService = Depends(),
):
    return pet_food_service.create(pet_food_body)


@router.put("/{id}", response_model=PetFoodGet, status_code=status.HTTP_200_OK)
def update_cat(
    id: int,
    pet_food_body: PetFoodCreateUpdate,
    pet_food_service: PetFoodService = Depends(),
):
    return pet_food_service.update(id, pet_food_body)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_cat(
    id: int,
    pet_food_service: PetFoodService = Depends(),
):
    pet_food_service.delete(id)
    return {"detail": "삭제되었습니다."}
