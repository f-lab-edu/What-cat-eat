from pydantic import BaseModel, Field
from fastapi import HTTPException
import re


class UserBase(BaseModel):
    nickname: str = Field(min_length=1, max_length=15)
    password: str
    password_check: str


class UserCreate(UserBase):
    user_id: str = Field(min_length=1, max_length=15)


class UserUpdate(UserBase):
    pass


class UserGet(BaseModel):
    id: int
    nickname: str

    class Config:
        orm_mode = True


def validate_password(values):
    if values.password_check != values.password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    if len(values.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호 길이가 너무 짧습니다.")

    if re.search(r"[a-z]", values.password) is None:
        raise HTTPException(
            status_code=400, detail="비밀번호는 한개 이상의 영소문자가 필수적으로 들어가야 합니다."
        )
    if re.search(r"\d", values.password) is None:
        raise HTTPException(
            status_code=400, detail="비밀번호는 한개 이상의 숫자가 필수적으로 들어가야 합니다."
        )

    return values.password