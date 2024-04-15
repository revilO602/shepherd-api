from typing import Annotated

from fastapi import Depends, HTTPException, status
from utils.auth_utils import oauth2_scheme
from app.config import settings
from app.schemas.auth import TokenData
from jose import JWTError, jwt
from app.services.auth import get_user
from exceptions.auth import CredentialsException

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise CredentialsException()
    return user
