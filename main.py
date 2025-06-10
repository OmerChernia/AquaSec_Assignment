from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import json
import re

app = FastAPI()

class UserBase(BaseModel):
    id: str = Field(..., min_length=9, max_length=9, description="The user's ID")
    name: str = Field(..., min_length=2, description="The user's name")
    phone: str = Field(..., description="The user's phone number")
    address: str = Field(..., description="The user's address")
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }

class UserCreate(UserBase):
    pass

class UserManager:
    def __init__(self):
        self.users: Dict[str, UserBase] = {}
        self.load_users()
        
    def validate_user_data(self, user_data: dict, index: int = None):
        """Validate a single user's data"""
        errors = []
        
        # Check required fields exist
        required_fields = ['id', 'name', 'phone', 'address']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                errors.append(f"Missing or empty {field}")
        
        if errors:
            user_info = f"User {index + 1}" if index is not None else "User"
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        # Validate ID
        try:
            self.validate_id(user_data['id'])
        except HTTPException as e:
            errors.append(f"Invalid ID: {e.detail}")
        
        # Validate phone
        try:
            self.validate_phone(user_data['phone'])
        except HTTPException as e:
            errors.append(f"Invalid phone: {e.detail}")
        
        # Validate name (minimum 2 characters)
        if len(user_data['name'].strip()) < 2:
            errors.append("Name must be at least 2 characters")
        
        # Validate address (not empty)
        if len(user_data['address'].strip()) == 0:
            errors.append("Address cannot be empty")
        
        if errors:
            user_info = f"User {index + 1} ({user_data.get('name', 'Unknown')})" if index is not None else f"User ({user_data.get('name', 'Unknown')})"
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        return True

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                users_list = json.load(file)
                
                print(f"Loading {len(users_list)} users from JSON...")
                valid_users = 0
                
                # Validate and convert each user
                for index, user_data in enumerate(users_list):
                    try:
                        # Validate the user data
                        self.validate_user_data(user_data, index)
                        
                        # Create UserBase object
                        user = UserBase(**user_data)
                        self.users[user.id] = user
                        valid_users += 1
                        
                    except ValueError as e:
                        print(f"Validation error: {e}")
                        continue
                    except Exception as e:
                        print(f"Error processing user {index + 1}: {e}")
                        continue
                
                print(f"Successfully loaded {valid_users}/{len(users_list)} users")
                    
        except FileNotFoundError:
            print("No users file found - starting with empty user list")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing users file: {e}")
            
        except Exception as e:
            print(f"Error loading users: {e}")
            
    def get_all_users(self):
        return list(self.users.values())
    
    def get_user_by_name(self, name: str):
        for user in self.users.values():
            if user.name == name:
                return user
        return None
    
    def get_all_usernames(self):
        return [user.name for user in self.users.values()]
    
    # --------- User Creation Methods ---------
    
    def save_users(self):
        # Save users to JSON file
        try:
            with open("users.json", "w") as file:
                # Convert Pydantic models to dictionaries
                users_data = [user.to_dict() for user in self.users.values()]
                json.dump(users_data, file, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def validate_id(self, id: str):
        if len(id) != 9:
            raise HTTPException(status_code=400, detail="ID must be 9 digits")
        if not id.isdigit():
            raise HTTPException(status_code=400, detail="ID must be a number")
        return id
    
    def validate_phone(self, phone: str):
        # Remove any spaces for validation
        phone = phone.replace(" ", "")
        
        # Define valid Israeli phone patterns
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
                
        # If no pattern matches, raise error
        raise HTTPException(
            status_code=400, 
            detail="Phone must be in format: 05X-XXXXXXX, 05XXXXXXXXX, +9725X-XXXXXXX, or +9725XXXXXXXXX"
        )
            
    def create_user(self, user: UserCreate):
        # Check if user already exists
        if user.id in self.users:
            print(f"User {user.id} already exists")
            raise HTTPException(status_code=400, detail="User already exists")
        
        self.validate_id(user.id)
        self.validate_phone(user.phone)
        
        # Add user to dictionary
        self.users[user.id] = user
        self.save_users()
        print(f"User {user.id} created")
        return user

# --------- User Manager ---------

user_manager = UserManager()
            
# --------- API Endpoints ---------

@app.get("/")
def read_root(): 
    return {"message": "Hello, World!"}

@app.get("/users", response_model=List[str])
def get_all_users():
    return user_manager.get_all_usernames()

@app.get("/users/{name}")
def get_user(name: str):
    return user_manager.get_user_by_name(name)

@app.post("/users", response_model=UserBase)
def create_user(user: UserCreate):
    return user_manager.create_user(user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=True)