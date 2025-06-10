"""
User API routes.
"""

from typing import List
from fastapi import APIRouter, Depends

from app.models.user import UserBase, UserCreate
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository


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


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    """Get user service instance with repository dependency."""
    return UserService(user_repository)


# Router
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[str], summary="Get all usernames", description="Retrieve a list of all usernames in the system")
def get_all_users(user_service: UserService = Depends(get_user_service)) -> List[str]:
    """Get all usernames."""
    return user_service.get_all_usernames()


@router.get("/{name}", response_model=UserBase, summary="Get user by name", description="Retrieve a specific user's information by their name")
def get_user(name: str, user_service: UserService = Depends(get_user_service)) -> UserBase:
    """
    Get user by name.
    
    Args:
        name: The user's name to search for
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    return user_service.get_user_by_name(name)


@router.post("/", response_model=UserBase, status_code=201, summary="Create new user", description="Create a new user with validation for ID and phone number formats")
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)) -> UserBase:
    """
    Create a new user.
    
    Args:
        user: User data to create
        
    Returns:
        The created user information
        
    Raises:
        HTTPException: If user already exists or validation fails
    """
    return user_service.create_user(user)