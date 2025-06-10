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

class userManager:
    def __init__(self):
        self.users: Dict[str, UserBase] = {}
        self.load_users()
        
    def load_users(self):
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
                
        except FileNotFoundError:
            print("No users file found")
            
        except json.JSONDecodeError:
            print("Error parsing users file")
            
    def get_all_users(self):
        return list(self.users.values())
    
    def get_user_by_id(self, id: str):
        return self.users.get(id)
            


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001)