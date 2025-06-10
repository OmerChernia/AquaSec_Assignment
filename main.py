from fastapi import FastAPI
import uvicorn

from app.config import settings
from app.routers import users_router
from app.repositories.user_repository import UserRepository
from app.routers.users import set_user_repository


# Create FastAPI application
app = FastAPI(title=settings.API_TITLE, description=settings.API_DESCRIPTION, version=settings.API_VERSION)

# Initialize repository at startup
user_repository = UserRepository(load_on_init=True)
set_user_repository(user_repository)

# Include routers
app.include_router(users_router)

# Root endpoint
@app.get("/", summary="Root endpoint", description="Returns a welcome message")
def read_root() -> dict:
    return {"message": "Welcome to AquaSec's Home Assignment API - Omer Chernia's solution!"}


# Application entry point
if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL)