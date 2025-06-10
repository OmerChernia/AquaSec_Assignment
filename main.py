"""
User Management API

A FastAPI-based REST API for managing users with data persistence.
Supports CRUD operations for users with validation for Israeli phone numbers and IDs.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
import re

# Constants
USERS_FILE = "users.json"
ID_LENGTH = 9
MIN_NAME_LENGTH = 2

app = FastAPI(
    title="User Management API",
    description="A REST API for managing users with Israeli phone number validation",
    version="1.0.0"
)

class UserBase(BaseModel):
    """ Base user model with validation rules. """
    
    id: str = Field(
        ..., 
        min_length=ID_LENGTH, 
        max_length=ID_LENGTH, 
        description="The user's 9-digit ID number"
    )
    name: str = Field(
        ..., 
        min_length=MIN_NAME_LENGTH, 
        description="The user's full name"
    )
    phone: str = Field(
        ..., 
        description="Israeli mobile phone number (israeli phone number format)"
    )
    address: str = Field(
        ..., 
        description="The user's address"
    )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }


class UserCreate(UserBase):
    """ Model for creating new users (inherits all validation from UserBase). """
    pass


class UserManager:
    """ Manages user data with file persistence and validation. """
    
    def __init__(self) -> None:
        """Initialize UserManager and load existing users from file."""
        self.users: Dict[str, UserBase] = {}
        self.invalid_users: List[dict] = []  # Store invalid users to preserve them
        self.load_users()
    
    # ========== DATA PERSISTENCE METHODS ==========
    
    def load_users(self) -> None:
        """
        Load users from JSON file with comprehensive validation.
        
        Validates each user's data and only loads valid entries.
        Invalid users are skipped with error reporting but preserved for saving.
        """
        try:
            with open(USERS_FILE, "r") as file:
                users_list = json.load(file)
                
                print(f"Loading {len(users_list)} users from {USERS_FILE}...")
                valid_users = 0
                
                for index, user_data in enumerate(users_list):
                    try:
                        self._validate_user_data(user_data)
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
            print(f"No {USERS_FILE} found - starting with empty user list")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing {USERS_FILE}: {e}")
            
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def save_users(self) -> None:
        """
        Save all users to JSON file.
        
        Saves both valid and invalid users to preserve original data.
        """
        try:
            with open(USERS_FILE, "w") as file:
                # Combine valid users and preserved invalid users
                valid_users_data = [user.to_dict() for user in self.users.values()]
                all_users_data = valid_users_data + self.invalid_users
                json.dump(all_users_data, file, indent=2)
                
        except Exception as e:
            print(f"Error saving users: {e}")
            raise HTTPException(status_code=500, detail="Failed to save user data")
    
    # ========== VALIDATION METHODS ==========
    
    def _validate_user_data(self, user_data: dict) -> bool:
        """
        Validate a single user's data from JSON.
        
        Args:
            user_data: Dictionary containing user information
            index: Optional index for error reporting
            
        Returns:
            True if validation passes
            
        Raises:
            ValueError: If validation fails with detailed error message
        """
        errors = []
        
        # Check required fields exist and are not empty
        required_fields = ['id', 'name', 'phone', 'address']
        for field in required_fields:
            if field not in user_data or not str(user_data[field]).strip():
                errors.append(f"Missing or empty {field}")
        
        if errors:
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        # Validate ID format
        try:
            self._validate_id(user_data['id'])
        except HTTPException as e:
            errors.append(f"Invalid ID: {e.detail}")
        
        # Validate phone format
        try:
            self._validate_phone(user_data['phone'])
        except HTTPException as e:
            errors.append(f"Invalid phone: {e.detail}")
        
        # Validate name length
        if len(user_data['name'].strip()) < MIN_NAME_LENGTH:
            errors.append(f"Name must be at least {MIN_NAME_LENGTH} characters")
        
        # Validate address is not empty
        if len(user_data['address'].strip()) == 0:
            errors.append("Address cannot be empty")
        
        if errors:
            user_info = (f"({user_data.get('name')})")
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        return True
    
    def _validate_id(self, user_id: str) -> str:
        """
        Validate Israeli ID number format.
        
        Args:
            user_id: ID string to validate
            
        Returns:
            The validated ID string
            
        Raises:
            HTTPException: If ID format is invalid
        """
        user_id = user_id.strip()
        
        if len(user_id) != ID_LENGTH:
            raise HTTPException(
                status_code=400, 
                detail=f"ID must be exactly {ID_LENGTH} digits"
            )
        
        if not user_id.isdigit():
            raise HTTPException(
                status_code=400, 
                detail="ID must contain only digits"
            )
        
        return user_id
    
    def _validate_phone(self, phone: str) -> str:
        """
        Validate Israeli mobile phone number format.
        
        Supports formats:
        - 05X-XXXXXXX (with dash)
        - 05XXXXXXXXX (without dash)  
        - +9725X-XXXXXXX (international with dash)
        - +9725XXXXXXXXX (international without dash)
        
        Args:
            phone: Phone number string to validate
            
        Returns:
            The validated phone string
            
        Raises:
            HTTPException: If phone format is invalid
        """
        # Remove spaces for validation
        phone = phone.replace(" ", "").strip()
        
        # Define valid Israeli mobile phone patterns
        patterns = [
            r'^05[0-9]-[0-9]{7}$',      # 05X-XXXXXXX
            r'^05[0-9]{8}$',            # 05XXXXXXXXX  
            r'^\+9725[0-9]-[0-9]{7}$',  # +9725X-XXXXXXX
            r'^\+9725[0-9]{8}$'         # +9725XXXXXXXXX
        ]
        
        # Check if phone matches any valid pattern
        for pattern in patterns:
            if re.match(pattern, phone):
                return phone
        
        # If no pattern matches, raise detailed error
        raise HTTPException(
            status_code=400, 
            detail="Phone must be in format: 05X-XXXXXXX, 05XXXXXXXXX, +9725X-XXXXXXX, or +9725XXXXXXXXX"
        )
    
    # ========== USER RETRIEVAL METHODS ==========
    
    def get_all_users(self) -> List[UserBase]:
        """
        Get all users as a list.
        
        Returns:
            List of all UserBase objects
        """
        return list(self.users.values())
    
    def get_all_usernames(self) -> List[str]:
        """
        Get all usernames as a list.
        
        Returns:
            List of all user names
        """
        return [user.name for user in self.users.values()]
    
    def get_user_by_id(self, user_id: str) -> Optional[UserBase]:
        """
        Get user by ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            UserBase object if found, None otherwise
        """
        return self.users.get(user_id)
    
    def get_user_by_name(self, name: str) -> Optional[UserBase]:
        """
        Get user by name (case-sensitive).
        
        Args:
            name: The user's name
            
        Returns:
            UserBase object if found, None otherwise
        """
        for user in self.users.values():
            if user.name == name:
                return user
        return None
    
    # ========== USER CREATION METHODS ==========
    
    def create_user(self, user: UserCreate) -> UserBase:
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
        self._validate_id(user.id)
        self._validate_phone(user.phone)
        
        # Add user to memory and save to file
        self.users[user.id] = user
        self.save_users()
        
        print(f"User {user.id} ({user.name}) created successfully")
        return user


# ========== GLOBAL INSTANCES ==========

user_manager = UserManager()


# ========== API ENDPOINTS ==========

@app.get("/", summary="Root endpoint", description="Returns a welcome message")
def read_root() -> dict:
    return {"message": "Welcome to AquaSec's Home Assignment API - Omer Chernia's solution!"}


@app.get("/users", response_model=List[str], summary="Get all usernames", description="Retrieve a list of all usernames in the system")
def get_all_users() -> List[str]:
    return user_manager.get_all_usernames()


@app.get("/users/{name}", response_model=UserBase, summary="Get user by name", description="Retrieve a specific user's information by their name")
def get_user(name: str) -> UserBase:
    """
    Get user by name.
    
    Args:
        name: The user's name to search for
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    user = user_manager.get_user_by_name(name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{name}' not found")
    return user


@app.post("/users", response_model=UserBase, status_code=201, summary="Create new user", description="Create a new user with validation for ID and phone number formats")
def create_user(user: UserCreate) -> UserBase:
    """
    Create a new user.
    
    Args:
        user: User data to create
        
    Returns:
        The created user information
        
    Raises:
        HTTPException: If user already exists or validation fails
    """
    return user_manager.create_user(user)


# ========== APPLICATION ENTRY POINT ==========

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001,log_level="info")