from pydantic import BaseModel


class Login(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
