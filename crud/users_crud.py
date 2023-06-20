from schemas.auth import UserOut, UserIn, UserAccessToken
from db.auth_model import Users, UserTokens
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pathlib import Path
from logs.custom_logging import CustomizeLogger

config_path = Path("logs/logging_config.json")
logger = CustomizeLogger.make_logger(config_path)


def create_user(user_info: UserIn, db: Session):
    try:
        user_model = Users()
        user_model.username = user_info.username
        user_model.email = user_info.email
        user_model.hashed_password = user_info.password
        user_model.description = user_info.description
        user_model.created_time = datetime.datetime.now()
        user_model.updated_time = datetime.datetime.now()

        db.add(user_model)
        db.commit()

        return 200, f"{user_info.username} creation successful"
    except IntegrityError as e:
        logger.error(f"error message: {e.args}")
        return 400, str(e.args)


def get_user(email: str, db: Session):
    user_result = UserOut
    result = db.query(Users).filter(Users.email == email).first()
    user_result.user_id = result.user_id
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


def create_token(token: UserAccessToken, db: Session):
    token_model = UserTokens()
    token_model.username = token.username
    token_model.user_token = token.user_token
    token_model.token_exp_date = token.token_expiration
    token_model.created_time = datetime.datetime.now()
    token_model.updated_time = datetime.datetime.now()

    db.add(token_model)
    db.commit()



