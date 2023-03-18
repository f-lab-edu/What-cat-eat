from repositories.CatRepository import CatRepository
from repositories.UserRepository import UserRepository
from fastapi import Depends, HTTPException
from schema.cat import CatCreate, CatUpdate
from models.cat import Cat
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CatService:
    catRepository: CatRepository
    userRepository: UserRepository

    def __init__(
        self,
        catRepository: CatRepository = Depends(),
        userRepository: UserRepository = Depends(),
    ) -> None:
        self.catRepository = catRepository
        self.userRepository = userRepository

    def get(self, id: int) -> Cat:
        cat = self.catRepository.get(id=id)
        if not cat:
            raise HTTPException(status_code=404, detail="해당 고양이를 찾을 수 없습니다.")
        return cat

    def create(self, cat_body: CatCreate, current_user_id: str) -> Cat:
        user = self.userRepository.get_user_by_user_id(current_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if cat_body.represent_cat and any(cat.represent_cat for cat in user.cats):
            raise HTTPException(status_code=409, detail="이미 대표 고양이가 있습니다.")

        return self.catRepository.create(
            Cat(
                id=cat_body.id,
                represent_cat=cat_body.represent_cat,
                name=cat_body.name,
                birth=cat_body.birth,
                gender=cat_body.gender,
                species=cat_body.species,
                weight=cat_body.weight,
                user_id=user.id,
                user=user,
            )
        )

    def update(self, id: int, cat_body: CatUpdate, current_user_id: str) -> Cat:
        cat = self.get(id)
        user = self.userRepository.get_user_by_user_id(current_user_id)

        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if cat.user.id != user.id:
            raise HTTPException(status_code=401, detail="user가 다릅니다. 권한이 없습니다.")

        if cat_body.represent_cat and any(cat.represent_cat for cat in user.cats):
            raise HTTPException(status_code=409, detail="이미 대표 고양이가 있습니다.")

        return self.catRepository.update(
            id,
            Cat(
                represent_cat=cat_body.represent_cat,
                name=cat_body.name,
                birth=cat_body.birth,
                gender=cat_body.gender,
                species=cat_body.species,
                weight=cat_body.weight,
                user_id=user.id,
            ),
        )

    def delete(self, id: int, current_user_id: int) -> None:
        cat = self.get(id)
        user = self.userRepository.get_user_by_user_id(current_user_id)

        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if not cat:
            raise HTTPException(status_code=404, detail="해당 고양이를 찾을 수 없습니다.")

        if cat.user.id != user.id:
            raise HTTPException(status_code=401, detail="user가 다릅니다. 권한이 없습니다.")

        return self.catRepository.delete(id)
