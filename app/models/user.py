"""
User Domain Models

Pydantic models for user data validation, serialization, and API documentation.
These models define the structure and validation rules for user data throughout the application.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
from app.config import settings
import re



class UserBase(BaseModel):
    """
    Base user model with comprehensive validation rules.
    
    This model defines the core user data structure and validation rules
    that apply to all user operations in the system.
    
    Attributes:
        id: 9-digit Israeli ID number (string format)
        name: User's full name (minimum 2 characters)
        phone: Israeli mobile phone number (various formats supported)
        address: User's address
    """
    
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
        """
        Convert user model to dictionary format.
        
        Useful for JSON serialization and database storage.
        
        Returns:
            Dict[str, str]: User data as dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }
        
class UserCreate(UserBase):
    """
    Model for creating new users.
    
    Inherits all validation rules from UserBase.
    This separate model allows for future extensibility where creation
    might have different validation rules or additional fields.
    
    Example usage:
        user_data = UserCreate(
            id="123456789",
            name="John Doe", 
            phone="050-1234567",
            address="123 Main St, Tel Aviv"
        )
    """
    pass
