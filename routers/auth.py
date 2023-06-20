from fastapi import Depends, APIRouter, Request, status
from schemas.auth import UserIn, User
from database import get_db
from sqlalchemy.orm import Session
from services import auth as auth_service
from templates.response_format import wrap_response
from pathlib import Path
from logs.custom_logging import CustomizeLogger

config_path = Path("logs/logging_config.json")
logger = CustomizeLogger.make_logger(config_path)

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/user")
def create_user(user: UserIn, db: Session = Depends(get_db)):
    """
    Create a user with all the information:

    - **username**: user name
    - **email**: user email (a unique value)
    - **password**: password
    - **description**: description
    """
    status_code, result = auth_service.create_user(user, db)

    if status_code == 200:
        logger.info("User creation successful")
        return wrap_response(status.HTTP_200_OK, result)
    else:
        logger.error("User creation failed")
        return wrap_response(status.HTTP_400_BAD_REQUEST, result, "BAD_REQUEST")


@router.post("/token")
def login(userinfo: User, db: Session = Depends(get_db)):
    """
    Information required to login:

    - **username**: user name
    - **email**: user email (a unique value)
    - **password**: password
    """
    result = auth_service.user_login(userinfo, db)
    if result:
        logger.info("Login Succeed")
        return wrap_response(status.HTTP_200_OK, result)
    else:
        logger.error("Login Failed")
        return wrap_response(
            status.HTTP_401_UNAUTHORIZED,
            "Login Failed")


@router.get("/users")
def get_user_list(request: Request, db: Session = Depends(get_db)):
    """
        Get all users:
    """
    if auth_service.validation_token(request):
        result = auth_service.get_users(db)
        logger.info("user list")
        return wrap_response(status.HTTP_200_OK, result)
    else:
        logger.error("Invalid token")
        return wrap_response(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token")


