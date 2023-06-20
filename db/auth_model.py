from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(length=20), index=True)
    email = Column(String(length=255), unique=True)
    hashed_password = Column(String(length=562))
    is_active = Column(Boolean, default=True)
    description = Column(String(length=1000))
    created_time = Column(DateTime(timezone=True))
    updated_time = Column(DateTime(timezone=True))


class UserTokens(Base):
    __tablename__ = "user_tokens"

    token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(length=20))
    user_token = Column(String(length=562))
    token_exp_date = Column(DateTime(timezone=True))
    created_time = Column(DateTime(timezone=True))
    updated_time = Column(DateTime(timezone=True))
