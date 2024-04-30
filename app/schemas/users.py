from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr | None = None

    class Config:
        from_attributes = True


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str
