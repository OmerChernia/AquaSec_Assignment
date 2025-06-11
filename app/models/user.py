from pydantic import BaseModel, Field
from typing import Dict
from app.config import settings



class UserBase(BaseModel):
    """Base user model with core fields and validation."""
    
    id: str = Field(
        ...,
        min_length= settings.ID_LENGTH,
        max_length=settings.ID_LENGTH,
        description="9-digit Israeli ID number",
    )
    
    name: str = Field(
        ...,
        min_length=settings.MIN_NAME_LENGTH,
        description="User's full name",
    )
    
    phone: str = Field(
        ...,
        description="Israeli mobile phone number (05X-XXXXXXX, 05XXXXXXXXX, +9725X-XXXXXXX, +9725XXXXXXXXX)",
    )
    
    address: str = Field(
        ...,
        min_length=1,
        description="User's physical address",
    )
    
    
    def to_dict(self) -> Dict[str, str]:
        """Converts the user object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }
        
class UserCreate(UserBase):
    """Model for creating a new user. Inherits from UserBase."""
    pass
