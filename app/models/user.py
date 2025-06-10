"""
User domain models.

Contains Pydantic models for user data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Dict


class UserBase(BaseModel):
    """Base user model with validation rules."""
    
    id: str = Field(
        ..., 
        min_length=9, 
        max_length=9, 
        description="The user's 9-digit ID number"
    )
    name: str = Field(
        ..., 
        min_length=2, 
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
    
    def to_dict(self) -> Dict[str, str]:
        """Convert user to dictionary format."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }


class UserCreate(UserBase):
    """Model for creating new users (inherits all validation from UserBase)."""
    pass