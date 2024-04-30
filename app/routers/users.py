from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies.users import get_current_user, unique_user
from app.schemas.users import User, UserIn
from app.services.users import insert_user
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import TokenWithUser

users_router = APIRouter()


@users_router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@users_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(unique_user)],
    response_model=TokenWithUser,
)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    return insert_user(user, db)
