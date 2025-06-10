"""
User repository for data persistence operations.
"""

import json
from typing import List, Optional, Dict
from fastapi import HTTPException

from app.models.user import UserBase, UserCreate
from app.repositories.base import BaseRepository
from app.config import settings
from app.utils.validators import UserValidator


class UserRepository(BaseRepository):
    """Handles user data persistence with file storage."""
    
    def __init__(self, load_on_init: bool = False):
        """Initialize repository and optionally load existing users."""
        self.users: Dict[str, UserBase] = {}
        self.invalid_users: List[dict] = []  # Store invalid users to preserve them
        if load_on_init:
            self.load_users()
    
    def load_users(self) -> None:
        """
        Load users from JSON file with comprehensive validation.
        
        Validates each user's data and only loads valid entries.
        Invalid users are skipped with error reporting but preserved for saving.
        """
        try:
            with open(settings.USERS_FILE, "r") as file:
                users_list = json.load(file)
                
                print(f"Loading {len(users_list)} users from {settings.USERS_FILE}...")
                valid_users = 0
                
                for index, user_data in enumerate(users_list):
                    try:
                        UserValidator.validate_user_data(user_data)
                        user = UserBase(**user_data)
                        self.users[user.id] = user
                        valid_users += 1
                        
                    except ValueError as e:
                        print(f"Validation error: {e}")
                        # Store invalid user to preserve in JSON
                        self.invalid_users.append(user_data)
                        continue
                    except Exception as e:
                        print(f"Error processing user {index + 1}: {e}")
                        # Store invalid user to preserve in JSON
                        self.invalid_users.append(user_data)
                        continue
                
                print(f"Successfully loaded {valid_users}/{len(users_list)} users")
                if self.invalid_users:
                    print(f"Preserved {len(self.invalid_users)} invalid users in memory")
                    
        except FileNotFoundError:
            print(f"No {settings.USERS_FILE} found - starting with empty user list")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing {settings.USERS_FILE}: {e}")
            
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def save_users(self) -> None:
        """
        Save all users to JSON file.
        
        Saves both valid and invalid users to preserve original data.
        """
        try:
            with open(settings.USERS_FILE, "w") as file:
                # Combine valid users and preserved invalid users
                valid_users_data = [user.to_dict() for user in self.users.values()]
                all_users_data = valid_users_data + self.invalid_users
                json.dump(all_users_data, file, indent=2)
                
        except Exception as e:
            print(f"Error saving users: {e}")
            raise HTTPException(status_code=500, detail="Failed to save user data")
    
    def get_all(self) -> List[UserBase]:
        """Get all users as a list."""
        return list(self.users.values())
    
    def get_by_id(self, user_id: str) -> Optional[UserBase]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def get_by_name(self, name: str) -> Optional[UserBase]:
        """Get user by name."""
        for user in self.users.values():
            if user.name == name:
                return user
        return None
    
    def get_all_names(self) -> List[str]:
        """Get all usernames as a list."""
        return [user.name for user in self.users.values()]
    
    def create(self, user: UserCreate) -> UserBase:
        """
        Create a new user with validation.
        
        Args:
            user: UserCreate object with user data
            
        Returns:
            The created UserBase object
            
        Raises:
            HTTPException: If user already exists or validation fails
        """
        # Check if user already exists
        if user.id in self.users:
            raise HTTPException(
                status_code=400, 
                detail=f"User with ID {user.id} already exists"
            )
        
        # Validate ID and phone formats
        UserValidator.validate_id(user.id)
        UserValidator.validate_phone(user.phone)
        
        # Add user to memory and save to file
        self.users[user.id] = user
        self.save_users()
        
        print(f"User {user.id} ({user.name}) created successfully")
        return user
    