from pydantic import BaseModel
from typing import Union


class Login(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Union[str, None] = None
