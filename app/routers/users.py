from typing import Annotated

from fastapi import APIRouter, Depends
from schemas.users import User
from dependencies.auth import get_current_user

users_router = APIRouter()


@users_router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@users_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
