from typing import Optional, Union
from fastapi import Request
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    description: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: str


class UserAccessToken(BaseModel):
    user_token: str
    username: str
    expired: str


class User(BaseModel):
    username: str
    email: str
    password: str



