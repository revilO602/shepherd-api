from datetime import timedelta
from app.models.user import User
from sqlalchemy import or_
from app.schemas.users import UserIn
from app.utils.auth_utils import create_access_token, get_password_hash
from sqlalchemy.orm import Session
from app.config import settings
from app.schemas.auth import TokenWithUser


def insert_user(user: UserIn, db: Session) -> None:
    db_user = User(
        **user.model_dump(exclude="password"),
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return TokenWithUser(access_token=access_token, user=db_user)


def get_user_email_or_username(username: str, email: str, db: Session) -> User:
    db_user = (
        db.query(User)
        .filter(or_(User.email == email, User.username == username))
        .first()
    )
    return db_user


def get_user_username(username: str, db: Session) -> User:
    db_user = db.query(User).filter(User.username == username).first()
    return db_user
