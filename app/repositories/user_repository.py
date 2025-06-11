import json
from typing import List, Optional, Dict
from fastapi import HTTPException

from app.models.user import UserBase, UserCreate
from app.repositories.base import BaseRepository
from app.config import settings
from app.utils.validators import UserValidator


class UserRepository(BaseRepository):
    """Handles user data persistence with file storage."""
    
    def __init__(self):
        """Initializes the repository and loads users from file."""
        self.users: Dict[str, UserBase] = {} # Stores valid users by ID
        self.invalid_users: List[dict] = []  # Stores user data that fails validation
        self.load_users()
    
    def load_users(self) -> None:
        """Loads and validates users from the JSON file."""
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
                        # Preserve invalid user data to avoid data loss on save
                        self.invalid_users.append(user_data)
                        continue
                    
                    except Exception as e:
                        print(f"Error processing user {index + 1}: {e}")
                        # Preserve invalid user data to avoid data loss on save
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
        """Saves all users (valid and invalid) back to the JSON file."""
        try:
            with open(settings.USERS_FILE, "w") as file:
                # Combine valid and invalid user lists to prevent data loss
                valid_users_data = [user.to_dict() for user in self.users.values()]
                all_users_data = valid_users_data + self.invalid_users
                json.dump(all_users_data, file, indent=2)
                
        except Exception as e:
            print(f"Error saving users: {e}")
            raise HTTPException(status_code=500, detail="Failed to save user data")
    
    # ----------- Abstract methods from BaseRepository -----------
    
    def get_all(self) -> List[UserBase]:
        """Gets all users as a list."""
        return list(self.users.values())
    
    def get_by_id(self, user_id: str) -> Optional[UserBase]:
        """Gets a user by their ID."""
        return self.users.get(user_id)
    
    def create(self, user: UserCreate) -> UserBase:
        """Creates a new user."""
        # Check if user already exists
        if user.id in self.users:
            raise HTTPException(
                status_code=400, 
                detail=f"User with ID {user.id} already exists"
            )
        
        # Validate ID and phone formats
        UserValidator.validate_id(user.id)
        UserValidator.validate_phone(user.phone)
        
        # Add to memory and save to file
        self.users[user.id] = user
        self.save_users()
        
        print(f"User {user.id} ({user.name}) created successfully")
        return user
    
    # ----------- Other methods -----------
    
    def get_by_name(self, name: str) -> Optional[UserBase]:
        """Gets a user by their name."""
        for user in self.users.values():
            if user.name == name:
                return user
        return None
    
    def get_all_names(self) -> List[str]:
        """Gets all usernames as a list."""
        return [user.name for user in self.users.values()]
    
    
    