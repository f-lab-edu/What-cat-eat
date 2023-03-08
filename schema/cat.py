from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class CatSpecies(str, Enum):
    KSH = "코리안 숏 헤어"
    BSH = "브리티시 숏 헤어"
    ASH = "아메리칸 숏 헤어"
    PE = "페르시안"
    MC = "메인 쿤"
    SI = "샴"
    RAG = "렉돌"
    SP = "스핑크스"
    AB = "아비니시안"
    BEN = "벵갈"
    EX = "엑조틱"
    RUS = "러시안블루"
    MUN = "먼치킨"


class CatBase(BaseModel):
    id: Optional[int] = Field(primary_key=True)
    represent_cat: bool = Field(default=False)
    name: str = Field(max_length=15)
    birth: date = None
    picture: str = None
    gender: Gender
    species: CatSpecies
    weight: int = Field(gt=0, description="몸무게는 0보다 같거나 커야합니다.")


class CatGet(CatBase):
    user_id: Optional[int]

    class Config:
        orm_mode = True


class CatCreate(CatBase):
    user: Optional[int] = None

    class Config:
        orm_mode = True


class CatUpdate(CatBase):
    pass
