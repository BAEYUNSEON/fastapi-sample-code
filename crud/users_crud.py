from schemas.auth import UserOut, UserIn
from db.auth_model import Users
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.exc import SQLAlchemyError


def create_user(user_info: UserIn, db: Session):
    try:
        user_model = Users()
        user_model.username = user_info.username
        user_model.email = user_info.email
        user_model.hashed_password = user_info.password

        db.add(user_model)
        db.commit()
        return {"Create User": "Successfully"}
    except SQLAlchemyError as e:
        return {"create_user": e.code}


def get_user(db: Session):
    user_result = UserOut
    result = db.query(Users).filter(Users.email == "yunseon.bae@gmail.com").first()
    user_result.username = result.username
    user_result.email = result.email

    return user_result


def get_user_by_email(email, db: Session):
    user = db.query(Users) \
        .filter(Users.email == email) \
        .first()

    return user


def get_user_list(db: Session):
    user_list = db.query(Users).all()

    return user_list

