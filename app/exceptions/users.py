from fastapi import HTTPException, status


class UserEmailNotUnqiue(HTTPException):
    def __init__(self, detail="Email already in use"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserUsernameNotUnqiue(HTTPException):
    def __init__(self, detail="Username already in exists"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
