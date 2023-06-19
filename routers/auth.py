from fastapi import Depends, APIRouter, Request
from schemas.auth import UserIn, User
from database import get_db
from sqlalchemy.orm import Session
from services import auth as auth_service


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
    """
    return auth_service.create_user(user, db)


@router.post("/token")
def login(userinfo: User, db: Session = Depends(get_db)):
    """
    Create a user with all the information:

    - **username**: user name
    - **email**: user email (a unique value)
    - **password**: password
    """
    return auth_service.user_login(userinfo, db)


@router.get("/users")
def get_user_list(request: Request, db: Session = Depends(get_db)):
    
    if auth_service.validation_token(request):
        return auth_service.get_users(db)
    else:
        return {"token": "expired"}


