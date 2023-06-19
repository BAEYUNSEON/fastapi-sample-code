from passlib.context import CryptContext
from fastapi import Depends, Request
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from schemas.auth import UserIn, User
from sqlalchemy.orm import Session
from crud import users_crud
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(user_email: str, password: str, db):
    user = users_crud.get_user_by_email(user_email, db)

    if not user:
        print("service.authenticate error")
        return False
    if not verify_password(password, user.hashed_password):
        print("verify false")
        return False
    return user


def create_user(userinfo: UserIn, db: Session):
    userinfo.password = bcrypt_context.hash(userinfo.password)
    result = users_crud.create_user(userinfo, db)

    return result


def create_access_token(username: str, user_id: int,
                        email: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id, "email": email}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def user_login(userinfo: User, db: Session):
    user = authenticate_user(userinfo.email, userinfo.password, db)

    if not user:
        return False

    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.user_id, user.email, expires_delta=token_expires)
    return {"Access Token": token}


def get_users(db: Session):
    result = users_crud.get_user_list(db)

    return {"Users": result}


def validation_token(request: Request):
    bearer_token = request.headers['authorization'].split('Bearer ')[1]
    print(" test=", bearer_token)
    payload = jwt.decode(bearer_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    exp_period = payload.get("exp")
    dt_object = datetime.fromtimestamp(exp_period)

    # test
    date_time_str = '2023-06-13 18:28:19'
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    print('Date-time:', date_time_obj)

    if date_time_obj > dt_object:
        print("expired token!")
        return False
    else:
        print("valid token!")
        return True






