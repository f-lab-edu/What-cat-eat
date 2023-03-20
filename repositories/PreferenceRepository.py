from repositories.RepositoryMeta import AbstractRepository
from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.preference import Allergy, PetFoodPreference
from schema.preference import AllergyGet, PetFoodPreferenceUpdate
from sqlalchemy.orm import joinedload


class PreferenceRepository(AbstractRepository):
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: int) -> PetFoodPreference:
        preference = (
            self.db.query(PetFoodPreference).filter(PetFoodPreference.id == id).first()
        )

        if not preference:
            return None
        return preference

    def get_all_my_cats_preferences(self, cat_id: int):
        preferences = (
            self.db.query(PetFoodPreference)
            .filter(PetFoodPreference.cat_id == cat_id)
            .options(joinedload(PetFoodPreference.allergies))
            .all()
        )
        print("여기까지 들어가는겨?3", preferences)
        if not preferences:
            return None
        return preferences

    def find_pet_food_preference(self, cat_id: int, pet_food_id: int):
        preference = (
            self.db.query(PetFoodPreference)
            .filter(
                PetFoodPreference.cat_id == cat_id,
                PetFoodPreference.pet_food_id == pet_food_id,
            )
            .first()
        )

        if not preference:
            return None
        return preference

    def create(self, petFoodPreference: PetFoodPreference) -> PetFoodPreference:
        self.db.add(petFoodPreference)
        self.db.commit()
        self.db.refresh(petFoodPreference)

        return petFoodPreference

    def update(self, update_preference: PetFoodPreferenceUpdate) -> PetFoodPreference:
        self.db.commit()
        self.db.refresh(update_preference)
        return update_preference

    def delete(self, id: int) -> None:
        preference = self.db.get(PetFoodPreference, id)
        self.db.delete(preference)
        self.db.commit()

    def get_allergy_by_condition(self, condition: AllergyGet):
        allergy = (
            self.db.query(Allergy)
            .filter(
                Allergy.allergy_name == condition.allergy_name,
            )
            .first()
        )
        return allergy

    def create_allergy(self, allergy: dict) -> Allergy:
        allergy_obj = Allergy(allergy_name=allergy.allergy_name)
        self.db.add(allergy_obj)
        self.db.commit()
        self.db.refresh(allergy_obj)
        return allergy_obj


class PreferenceFakeRepository(AbstractRepository):
    def __init__(self):
        self._preference = []
        self._allergy = []
        self._preference_allergy = {}

    def get(self, id) -> PetFoodPreference:
        if len(self._preference) < id:
            return None
        preference = self._preference[id - 1]
        return preference

    def get_all_my_cats_preferences(self, cat_id: int) -> list:
        preferences = []

        for preference in self._preference:
            if preference.cat_id == cat_id:
                preferences.append(preference)

        return preferences

    def find_pet_food_preference(
        self, cat_id: int, pet_food_id: int
    ) -> PetFoodPreference:
        for preference in self._preference:
            if preference.cat_id == cat_id and preference.pet_food_id == pet_food_id:
                return preference
        return None

    def create(self, preference: PetFoodPreference) -> PetFoodPreference:
        preference.id = len(self._preference) + 1
        self._preference.append(preference)

        allergy_value = self._preference_allergy.get(len(self._preference) - 1, [])

        for allergy in preference.allergies:
            allergy_value.append(allergy)

        self._preference_allergy[len(self._preference) - 1] = allergy_value
        return preference

    def update(self, update_preference: PetFoodPreference) -> PetFoodPreference:
        self._preference[update_preference.id - 1] = update_preference

        allergy_value = self._preference_allergy.get(len(self._preference) - 1, [])

        for allergy in update_preference.allergies:
            allergy_value.append(allergy)

        self._preference_allergy[len(self._preference) - 1] = allergy_value

        preference = self._preference[update_preference.id - 1]
        print("여기확인용ㅇㅇ ", preference.preference, update_preference.preference)
        return preference

    def delete(self, id: int) -> None:
        del self._preference[id - 1]
        return len(self._preference)
