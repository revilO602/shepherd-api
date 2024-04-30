from pydantic import BaseModel
from app.schemas.users import User


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class TokenWithUser(Token):
    user: User | None = None
