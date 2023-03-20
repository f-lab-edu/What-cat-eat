from fastapi import APIRouter, Depends, status
from services.PreferenceService import PreferenceService
from schema.preference import (
    PetFoodPreferenceGet,
    PetFoodPreferenceCreate,
    PetFoodPreferenceUpdate,
)
from typing import List

router = APIRouter(
    prefix="/petfood/preference",
)


@router.get(
    "/{id}", response_model=PetFoodPreferenceGet, status_code=status.HTTP_200_OK
)
def get_preference(id: int, preference_service: PreferenceService = Depends()):
    return preference_service.get(id)


@router.get(
    "", response_model=List[PetFoodPreferenceGet], status_code=status.HTTP_200_OK
)
def get_all_preferences(cat_id: int, preference_service: PreferenceService = Depends()):
    return preference_service.get_all_my_cats_preferences(cat_id=cat_id)


@router.post(
    "", response_model=PetFoodPreferenceGet, status_code=status.HTTP_201_CREATED
)
def create_preference(
    preference_body: PetFoodPreferenceCreate,
    preference_service: PreferenceService = Depends(),
):

    return preference_service.create(preference_body)


@router.put(
    "/{id}", response_model=PetFoodPreferenceGet, status_code=status.HTTP_200_OK
)
def update_preference(
    id: int,
    preference_body: PetFoodPreferenceUpdate,
    preference_service: PreferenceService = Depends(),
):
    return preference_service.update(id, preference_body)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_preference(
    id: int,
    preference_service: PreferenceService = Depends(),
):
    preference_service.delete(id)
    return {"detail": "삭제되었습니다."}
