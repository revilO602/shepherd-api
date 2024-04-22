from app.services.users import get_user_username
from app.utils.auth_utils import verify_password
from sqlalchemy.orm import Session


def authenticate_user(username: str, password: str, db: Session):
    user = get_user_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
