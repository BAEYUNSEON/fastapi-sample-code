from typing import Union
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    description: Union[str, None] = None


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str


class UserAccessToken(BaseModel):
    user_token: str
    username: str
    token_expiration: str


class User(BaseModel):
    username: str
    email: str
    password: str



