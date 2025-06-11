from typing import List
from fastapi import APIRouter, Depends

from app.models.user import UserBase, UserCreate
from app.repositories.user_repository import UserRepository


# ---------- Global repository instance ----------

# Global repository instance (initialized at startup)
_user_repository = None


def set_user_repository(repository: UserRepository) -> None:
    """Set the global user repository instance."""
    global _user_repository
    _user_repository = repository


# Dependency injection
def get_user_repository() -> UserRepository:
    """Get user repository instance."""
    return _user_repository

# -------------------------------------------------


# Router
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[str], summary="Get all usernames", description="Retrieve a list of all usernames in the system")
def get_all_users(user_repository: UserRepository = Depends(get_user_repository)) -> List[str]:
    """Get all usernames."""
    return user_repository.get_all_names()


@router.get("/{name}", response_model=UserBase, summary="Get user by name", description="Retrieve a specific user's information by their name")
def get_user(name: str, user_repository: UserRepository = Depends(get_user_repository)) -> UserBase:
    """Gets a single user by their name."""
    return user_repository.get_by_name(name)


@router.post("/", response_model=UserBase, status_code=201, summary="Create new user", description="Create a new user with validation for ID and phone number formats")
def create_user(user: UserCreate, user_repository: UserRepository = Depends(get_user_repository)) -> UserBase:
    """Creates a new user."""
    return user_repository.create(user)