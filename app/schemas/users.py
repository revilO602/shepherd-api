from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr | None = None


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str
