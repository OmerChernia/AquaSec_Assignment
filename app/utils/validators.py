import re
from typing import Dict
from fastapi import HTTPException

from app.config import settings


class UserValidator:
    """A collection of static methods for validating user data."""
    
    @staticmethod
    def validate_user_data(user_data: Dict) -> bool:
        """Checks if a user data dictionary is valid."""
        errors = []
        
        # Check that required fields exist and are not empty
        required_fields = ['id', 'name', 'phone', 'address']
        for field in required_fields:
            if field not in user_data or not str(user_data[field]).strip():
                errors.append(f"Missing or empty {field}")
        
        if errors:
            user_info = f"({user_data.get('name', 'Unknown')})"
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        # Validate ID format
        try:
            UserValidator.validate_id(user_data['id'])
        except HTTPException as e:
            errors.append(f"Invalid ID: {e.detail}")
        
        # Validate phone format
        try:
            UserValidator.validate_phone(user_data['phone'])
        except HTTPException as e:
            errors.append(f"Invalid phone: {e.detail}")
        
        # Validate name length
        if len(user_data['name'].strip()) < settings.MIN_NAME_LENGTH:
            errors.append(f"Name must be at least {settings.MIN_NAME_LENGTH} characters")
        
        # Validate address is not empty
        if len(user_data['address'].strip()) == 0:
            errors.append("Address cannot be empty")
        
        if errors:
            user_info = f"({user_data.get('name', 'Unknown')})"
            raise ValueError(f"{user_info}: {', '.join(errors)}")
        
        return True
    
    @staticmethod
    def validate_id(user_id: str) -> str:
        """Validates the format of an Israeli ID number."""
        user_id = user_id.strip()
        
        if len(user_id) != settings.ID_LENGTH:
            raise HTTPException(
                status_code=400, 
                detail=f"ID must be exactly {settings.ID_LENGTH} digits"
            )
        
        if not user_id.isdigit():
            raise HTTPException(
                status_code=400, 
                detail="ID must contain only digits"
            )
        
        return user_id
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        """
        Validate Israeli mobile phone number format.
        
        Supports:
        - 05X-XXXXXXX
        - 05XXXXXXXXX
        - +9725X-XXXXXXX
        - +9725XXXXXXXXX
        """
        phone = phone.replace(" ", "").strip()
        
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