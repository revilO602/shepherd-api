from app.models.user import User
from sqlalchemy import or_
from app.schemas.users import UserIn
from app.utils.auth_utils import get_password_hash
from sqlalchemy.orm import Session


def insert_user(user: UserIn, db: Session) -> None:
    db_user = User(
        **user.model_dump(exclude="password"),
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return


def get_user_email_or_username(username: str, email: str, db: Session) -> User:
    db_user = (
        db.query(User)
        .filter(or_(User.email == email, User.username == username))
        .first()
    )
    return db_user


def get_user_username(username: str, db: Session) -> User:
    db_user = db.query(User).filter(or_(User.username == username)).first()
    return db_user
