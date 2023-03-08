import pytest
from fastapi import HTTPException
from tests.conftest import MOCK_PET_FOOD
from models.pet_food import PetFood, Nutrient, Component


def test_get_nonexistent_pet_food(mock_pet_food_service):
    with pytest.raises(HTTPException) as response:
        mock_pet_food_service.get(999999)

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 404
    assert response.value.detail == "해당 사료를 찾을 수 없습니다."


def test_get_pet_food(mock_pet_food_service):
    pet_food = mock_pet_food_service.get(MOCK_PET_FOOD.id)
    assert pet_food.id == 1
    assert pet_food.name == "맛있는 사료"


def test_get_all_pet_foods(mock_pet_food_service_new):
    pet_foods = mock_pet_food_service_new.get_all_pet_foods()

    assert len(pet_foods) == 2


def test_create_duplicate_pet_foods_name(mock_pet_food_service):
    with pytest.raises(HTTPException) as response:
        mock_pet_food_service.create(
            PetFood(
                name="맛있는 사료",
                nutrients=[
                    Nutrient(nutrient_name="칼슘", percentage=5, is_above=False),
                    Nutrient(nutrient_name="조지방", percentage=10, is_above=True),
                ],
                components=[Component(component_name="닭")],
            )
        )
    assert response.value.status_code == 409
    assert response.value.detail == "해당 사료는 이미 존재합니다."


def test_create_pet_food(mock_pet_food_service):
    pet_food = mock_pet_food_service.create(
        PetFood(
            name="맛없는 사료",
            nutrients=[
                Nutrient(nutrient_name="칼슘", percentage=5, is_above=False),
                Nutrient(nutrient_name="조지방", percentage=10, is_above=True),
            ],
            components=[Component(component_name="닭")],
        )
    )
    assert pet_food.id == 2
    assert pet_food.name == "맛없는 사료"
    assert pet_food.nutrients[0].nutrient_name == "칼슘"
    assert pet_food.components[0].component_name == "닭"


def test_update_pet_food(mock_pet_food_service):
    pet_food = mock_pet_food_service.update(
        MOCK_PET_FOOD.id,
        pet_food_body=PetFood(
            name="맛있게 먹는 사료(수정)",
        ),
    )

    assert pet_food.id == 1
    assert pet_food.name == "맛있게 먹는 사료(수정)"


def test_delete_pet_food(mock_pet_food_service):
    pet_food_len = mock_pet_food_service.delete(
        MOCK_PET_FOOD.id,
    )

    assert pet_food_len == 0
