from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict
import json

app = FastAPI()

class UserBase(BaseModel):
    id: str = Field(..., min_length=9, max_length=9, description="The user's ID")
    name: str = Field(..., min_length=2, description="The user's name")
    phone: str = Field(..., description="The user's phone number")
    address: str = Field(..., description="The user's address")

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
            
        except json.JSONDecodeError:
            print("Error parsing users file")
            
    def get_all_users(self):
        return list(self.users.values())
    
    def get_user_by_name(self, name: str):
        for user in self.users.values():
            if user.name == name:
                return user
        return None
    
# --------- User Manager ---------

user_manager = UserManager()
            
# --------- API Endpoints ---------

@app.get("/")
def read_root(): 
    return {"message": "Hello, World!"}

@app.get("/users", response_model=List[UserBase])
def get_all_users():
    return user_manager.get_all_users()

@app.get("/users/{name}")
def get_user(name: str):
    return user_manager.get_user_by_name(name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001)