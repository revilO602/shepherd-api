from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from app.schemas.auth import Token
from app.services.auth import authenticate_user
from app.exceptions.auth import UnauthorizedException
from app.utils.auth_utils import create_access_token
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

auth_router = APIRouter()


@auth_router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise UnauthorizedException()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
