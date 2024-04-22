from fastapi import APIRouter, Depends, status
from app.dependencies.users import unique_user
from app.schemas.users import UserIn
from app.services.users import insert_user
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

users_router = APIRouter()


@users_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(unique_user)],
    response_model=None,
)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    insert_user(user, db)
    return
