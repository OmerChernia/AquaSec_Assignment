"""
User service layer for business logic.
"""

from typing import List, Optional
from fastapi import HTTPException

from app.models.user import UserBase, UserCreate
from app.repositories.user_repository import UserRepository


class UserService:
    
    def __init__(self, user_repository: UserRepository):
        """Initialize service with repository dependency."""
        self.user_repository = user_repository
    
    def get_all_users(self) -> List[UserBase]:
        """Get all users."""
        return self.user_repository.get_all()
    
    def get_all_usernames(self) -> List[str]:
        """Get all usernames."""
        return self.user_repository.get_all_names()
    
    def get_user_by_id(self, user_id: str) -> Optional[UserBase]:
        """Get user by ID."""
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_name(self, name: str) -> UserBase:
        """
        Get user by name with error handling.
        
        Args:
            name: The user's name to search for
            
        Returns:
            User information
            
        Raises:
            HTTPException: If user not found
        """
        user = self.user_repository.get_by_name(name)
        if not user:
            raise HTTPException(status_code=404, detail=f"User '{name}' not found")
        return user
    
    def create_user(self, user_data: UserCreate) -> UserBase:
        """
        Create a new user.
        
        Args:
            user_data: User data to create
            
        Returns:
            The created user information
            
        Raises:
            HTTPException: If user already exists or validation fails
        """
        return self.user_repository.create(user_data)
    