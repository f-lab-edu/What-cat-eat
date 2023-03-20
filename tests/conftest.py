import pytest
from datetime import datetime
from passlib.context import CryptContext
from models.user import User
from models.cat import Cat
from models.preference import PetFoodPreference, Allergy
from models.pet_food import PetFood, Nutrient, Component
from repositories import (
    UserRepository,
    CatRepository,
    PetFoodRepository,
    PreferenceRepository,
)
from services.LoginService import LoginService
from services.UserServices import UserService
from services.CatServices import CatService
from services.PetFoodService import PetFoodService
from services.PreferenceService import PreferenceService

MOCK_TEST_USER = User(
    id=1,
    user_id="test_id",
    password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("test1234"),
    nickname="test_nickname",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    cats=[],
)

MOCK_TEST_USER_NEW = User(
    id=2,
    user_id="test_id2",
    password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("test1234"),
    nickname="test_nickname2",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    cats=[],
)

MOCK_TEST_CAT = Cat(
    id=1,
    represent_cat=True,
    name="test_cat",
    birth=datetime.now(),
    gender="Male",
    species="코리안 숏 헤어",
    weight=5,
    user_id=MOCK_TEST_USER.id,
    user=MOCK_TEST_USER,
)


MOCK_NUTRIENT = Nutrient(nutrient_name="지방", percentage=10, is_above=True)

MOCK_COMPONENT = Component(component_name="참치")

MOCK_PET_FOOD_1 = PetFood(
    id=1, name="맛있는 사료", nutrients=[MOCK_NUTRIENT], components=[MOCK_COMPONENT]
)

MOCK_PET_FOOD_2 = PetFood(
    id=2, name="건강한 사료", nutrients=[MOCK_NUTRIENT], components=[MOCK_COMPONENT]
)

MOCK_PET_FOOD_3 = PetFood(
    id=3, name="맛동산 사료", nutrients=[MOCK_NUTRIENT], components=[MOCK_COMPONENT]
)

MOCK_ALLERGY = Allergy(id=1, allergy_name="결막염")

MOCK_ALLERGY_NEW = Allergy(id=2, allergy_name="구토")

MOCK_PREFERENCE = PetFoodPreference(
    id=1,
    preference="good",
    memo="아주 잘 먹어요",
    allergies=[MOCK_ALLERGY],
    pet_food_id=MOCK_PET_FOOD_1.id,
    pet_food=MOCK_PET_FOOD_1,
    cat_id=MOCK_TEST_CAT.id,
    cat=MOCK_TEST_CAT,
)

MOCK_PREFERENCE_NEW = PetFoodPreference(
    id=2,
    preference="bad",
    memo="먹다가 토함",
    allergies=[MOCK_ALLERGY_NEW],
    pet_food_id=MOCK_PET_FOOD_2.id,
    pet_food=MOCK_PET_FOOD_2,
    cat_id=MOCK_TEST_CAT.id,
    cat=MOCK_TEST_CAT,
)


def mock_user_fake_repository():
    user_repository = UserRepository.UserFakeRepository()
    user_repository.create(MOCK_TEST_USER)
    return user_repository


def mock_cat_fake_repository():
    user = mock_user_fake_repository()
    cat_repository = CatRepository.CatFakeRepository(user)
    cat_repository.create(MOCK_TEST_CAT)
    return cat_repository


def mock_fake_repository_with_new_member():
    user_repository = UserRepository.UserFakeRepository()
    user_repository.create(MOCK_TEST_USER)
    user_repository.create(MOCK_TEST_USER_NEW)
    return user_repository


def mock_cat_fake_repository_with_new_member():
    user = mock_fake_repository_with_new_member()
    cat_repository = CatRepository.CatFakeRepository(user)
    cat_repository.create(MOCK_TEST_CAT)
    return cat_repository


def mock_pet_food_repository():
    pet_food_repository = PetFoodRepository.PetFoodFakeRepository()
    pet_food_repository.create(MOCK_PET_FOOD_1)
    return pet_food_repository


def mock_pet_food_repository_with_new_pet_food():
    pet_food_repository = PetFoodRepository.PetFoodFakeRepository()
    pet_food_repository.create(MOCK_PET_FOOD_1)
    pet_food_repository.create(MOCK_PET_FOOD_2)
    pet_food_repository.create(MOCK_PET_FOOD_3)
    return pet_food_repository


def mock_preference_repository():
    preference_repository = PreferenceRepository.PreferenceFakeRepository()
    preference_repository.create(MOCK_PREFERENCE)
    preference_repository.create(MOCK_PREFERENCE_NEW)
    return preference_repository


@pytest.fixture(autouse=True)
def mock_user_service():
    return UserService(userRepository=mock_user_fake_repository())


@pytest.fixture(autouse=True)
def mock_user_service_new():
    return UserService(userRepository=mock_fake_repository_with_new_member())


@pytest.fixture(autouse=True)
def mock_login_service():
    return LoginService(userRepository=mock_user_fake_repository())


@pytest.fixture(autouse=True)
def mock_cat_service():
    return CatService(
        catRepository=mock_cat_fake_repository(),
        userRepository=mock_user_fake_repository(),
    )


@pytest.fixture(autouse=True)
def mock_cat_service_new():
    return CatService(
        catRepository=mock_cat_fake_repository_with_new_member(),
        userRepository=mock_fake_repository_with_new_member(),
    )


@pytest.fixture(autouse=True)
def mock_pet_food_service():
    return PetFoodService(pet_food_repository=mock_pet_food_repository())


@pytest.fixture(autouse=True)
def mock_pet_food_service_new():
    return PetFoodService(
        pet_food_repository=mock_pet_food_repository_with_new_pet_food()
    )


@pytest.fixture(autouse=True)
def mock_preference_service():
    return PreferenceService(
        preference_repository=mock_preference_repository(),
        catRepository=mock_cat_fake_repository(),
        petfoodRepository=mock_pet_food_repository_with_new_pet_food(),
    )
