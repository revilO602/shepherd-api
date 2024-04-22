from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import auth_router
from app.routers.users import users_router
from app.routers.trips import trips_router
from app.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(auth_router)
app.include_router(users_router, prefix="/users")
app.include_router(trips_router, prefix="/trips")


@app.get("/")
async def root():
    return {"message": "Hello World"}
