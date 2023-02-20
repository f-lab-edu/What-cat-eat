from datetime import datetime
import pytest
from passlib.context import CryptContext

from models.user import User
from models.cat import Cat
from repositories import UserRepository, CatRepository
from services.LoginService import LoginService
from services.UserServices import UserService
from services.CatServices import CatService

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
    return CatService(catRepository=mock_cat_fake_repository())


@pytest.fixture(autouse=True)
def mock_cat_service_new():
    return CatService(catRepository=mock_cat_fake_repository_with_new_member())
