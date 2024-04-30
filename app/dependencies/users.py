from typing import Annotated
from fastapi import Depends
from app.schemas.users import UserIn
from app.services.users import get_user_email_or_username, get_user_username
from app.exceptions.users import UserEmailNotUnqiue
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth_utils import oauth2_scheme
from jose import JWTError, jwt
from app.exceptions.auth import CredentialsException
from app.config import settings
from app.schemas.auth import TokenData


def unique_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = get_user_email_or_username(user.username, user.email, db)
    if db_user:
        if user.email == db_user.email:
            raise UserEmailNotUnqiue()
        if user.username == db_user.username:
            raise UserEmailNotUnqiue()
    return db_user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException()
    user = get_user_username(token_data.username, db)
    if user is None:
        raise CredentialsException()
    return user
