from repositories.PreferenceRepository import PreferenceRepository
from repositories.PetFoodRepository import PetFoodRepository
from repositories.CatRepository import CatRepository
from fastapi import Depends, HTTPException
from schema.preference import (
    PetFoodPreferenceGet,
    PetFoodPreferenceCreate,
    PetFoodPreferenceUpdate,
)
from models.preference import PetFoodPreference


class PreferenceService:
    preference_repository: PreferenceRepository
    catRepository: CatRepository
    petfoodRepository: PetFoodRepository

    def __init__(
        self,
        preference_repository: PreferenceRepository = Depends(),
        catRepository: CatRepository = Depends(),
        petfoodRepository: PetFoodRepository = Depends(),
    ) -> None:
        self.preference_repository = preference_repository
        self.catRepository = catRepository
        self.petfoodRepository = petfoodRepository

    def get(self, id: int) -> PetFoodPreferenceGet:
        preference = self.preference_repository.get(id=id)
        if not preference:
            raise HTTPException(status_code=404, detail="해당 사료와 관련된 선호도를 찾을 수 없습니다.")
        return preference

    def get_all_my_cats_preferences(self, cat_id: int):
        preferences = self.preference_repository.get_all_my_cats_preferences(cat_id)
        return preferences

    def create(self, preference_body: PetFoodPreferenceCreate) -> PetFoodPreference:
        pet_food_id = preference_body.pet_food_id
        cat_id = preference_body.cat_id

        find_pet_food_preference = self.preference_repository.find_pet_food_preference(
            cat_id,
            pet_food_id,
        )

        if find_pet_food_preference:
            raise HTTPException(status_code=409, detail="해당 사료에 관한 선호도는 이미 존재합니다.")

        cat = self.catRepository.get(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="해당 고양이를 찾을 수 없습니다.")

        pet_food = self.petfoodRepository.get(pet_food_id)
        if not pet_food:
            raise HTTPException(status_code=404, detail="해당 사료를 찾을 수 없습니다.")

        allergies = self.finding_allergy(preference_body.allergies)
        return self.preference_repository.create(
            PetFoodPreference(
                cat_id=cat_id,
                cat=cat,
                pet_food_id=pet_food,
                pet_food=pet_food,
                preference=preference_body.preference,
                memo=preference_body.memo,
                allergies=allergies,
            )
        )

    def update(
        self, id: int, preference_body: PetFoodPreferenceUpdate
    ) -> PetFoodPreference:
        pet_food_preference = self.get(id)

        if preference_body.allergies:
            pet_food_preference.allergies = self.finding_allergy(
                preference_body.allergies
            )

        pet_food_preference.preference = preference_body.preference
        pet_food_preference.memo = preference_body.memo

        return self.preference_repository.update(update_preference=pet_food_preference)

    def delete(self, id: int) -> None:
        pet_food_preference = self.get(id)
        if pet_food_preference:
            return self.preference_repository.delete(id)

    def finding_allergy(self, preference_allergies: list) -> list:
        allergies = []

        for allergy in preference_allergies:
            allergy_obj = self.preference_repository.get_allergy_by_condition(allergy)
            if not allergy_obj:
                allergy_obj = self.preference_repository.create_allergy(allergy)

            if allergy_obj not in preference_allergies:
                allergies.append(allergy_obj)

        return allergies
