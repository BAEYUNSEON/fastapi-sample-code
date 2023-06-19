from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(length=20), index=True)
    email = Column(String(length=255), unique=True)
    hashed_password = Column(String(length=562))
    is_active = Column(Boolean, default=True)
    created_time = Column(DateTime(timezone=True))
    changed_time = Column(DateTime(timezone=True))


class UserTokens(Base):
    __tablename__ = "user_tokens"

    token_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_token = Column(String(length=562))
    username = Column(String(length=20))
    expired = Column(String(length=20))
    created_time = Column(DateTime(timezone=True))
    changed_time = Column(DateTime(timezone=True))
