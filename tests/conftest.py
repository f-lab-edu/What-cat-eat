import pytest
from datetime import datetime
from passlib.context import CryptContext
from models.user import User
from models.cat import Cat
from models.pet_food import PetFood, Nutrient, Component
from repositories import UserRepository, CatRepository, PetFoodRepository
from services.LoginService import LoginService
from services.UserServices import UserService
from services.CatServices import CatService
from services.PetFoodService import PetFoodService

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

MOCK_PET_FOOD = PetFood(
    id=1, name="맛있는 사료", nutrients=[MOCK_NUTRIENT], components=[MOCK_COMPONENT]
)

MOCK_PET_FOOD_NEW = PetFood(
    id=2, name="건강한 사료", nutrients=[MOCK_NUTRIENT], components=[MOCK_COMPONENT]
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
    pet_food_repository.create(MOCK_PET_FOOD)
    return pet_food_repository


def mock_pet_food_repository_with_new_pet_food():
    pet_food_repository = PetFoodRepository.PetFoodFakeRepository()
    pet_food_repository.create(MOCK_PET_FOOD)
    pet_food_repository.create(MOCK_PET_FOOD_NEW)
    return pet_food_repository


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
