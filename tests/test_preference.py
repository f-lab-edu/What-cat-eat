import pytest
from fastapi import HTTPException
from tests.conftest import (
    MOCK_PREFERENCE,
    MOCK_TEST_CAT,
    MOCK_PET_FOOD_1,
    MOCK_PET_FOOD_3,
)
from models.preference import PetFoodPreference


def test_get_nonexistent_preference(mock_preference_service):
    with pytest.raises(HTTPException) as response:
        mock_preference_service.get(999999)

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 404
    assert response.value.detail == "해당 사료와 관련된 선호도를 찾을 수 없습니다."


def test_get_perference(mock_preference_service):
    preference = mock_preference_service.get(MOCK_PREFERENCE.id)
    assert preference.id == 1
    assert preference.preference == "good"


def test_get_all_my_cats_preferences(mock_preference_service):
    preferences = mock_preference_service.get_all_my_cats_preferences(MOCK_TEST_CAT.id)

    assert len(preferences) == 2


def test_create_duplicate_preference(mock_preference_service):
    with pytest.raises(HTTPException) as response:
        mock_preference_service.create(
            preference_body=PetFoodPreference(
                preference="good",
                memo="아주 잘 먹어요",
                pet_food_id=MOCK_PET_FOOD_1.id,
                pet_food=MOCK_PET_FOOD_1,
                cat_id=MOCK_TEST_CAT.id,
                cat=MOCK_TEST_CAT,
            ),
        )
    assert response.value.status_code == 409
    assert response.value.detail == "해당 사료에 관한 선호도는 이미 존재합니다."


def test_create_pet_food(mock_preference_service):
    preference = mock_preference_service.create(
        preference_body=PetFoodPreference(
            preference="good",
            memo="사료를 너무 좋아해요",
            pet_food_id=MOCK_PET_FOOD_3.id,
            pet_food=MOCK_PET_FOOD_3,
            cat_id=MOCK_TEST_CAT.id,
            cat=MOCK_TEST_CAT,
        ),
    )
    assert preference.id == 3
    assert preference.preference == "good"
    assert preference.pet_food.name == "맛동산 사료"
    assert preference.cat.name == "test_cat"


def test_update_pet_food(mock_preference_service):
    preference = mock_preference_service.update(
        MOCK_PREFERENCE.id,
        preference_body=PetFoodPreference(preference="neutral", memo="맛은 있어하나 눈을 긁는다."),
    )

    assert preference.id == 1
    assert preference.preference == "neutral"
    assert preference.memo == "맛은 있어하나 눈을 긁는다."


def test_delete_pet_food(mock_preference_service):
    preference_len = mock_preference_service.delete(
        MOCK_PREFERENCE.id,
    )

    assert preference_len == 1
