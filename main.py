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
        
    def load_users(self):
        try:
            with open("users.json", "r") as file:
                users_list = json.load(file)
                # Convert list of users to dictionary with ID as key
                for user_data in users_list:
                    user = UserBase(**user_data)
                    self.users[user.id] = user
                    
        except FileNotFoundError:
            print("No users file found")
            
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
        
        # Add user to dictionary
        if not self.validate_id(user.id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        
        if not self.validate_phone(user.phone):
            raise HTTPException(status_code=400, detail="Invalid phone number")
        
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