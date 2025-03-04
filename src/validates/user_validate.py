from typing import List, Optional, Tuple
from fastapi import UploadFile
import re

def validate_user_form(
    name: Optional[str], 
    age: Optional[int], 
    email: Optional[str], 
    phone: Optional[str], 
    password: Optional[str], 
    avatar: Optional[UploadFile]
) -> List[str]:

    """
    Kiểm tra định dạng của từng trường dữ liệu mà người dùng nhập vào 
    """

    errors = []
    
    # Name validation
    if not name or not name.strip():
        errors.append("Name is required.")
    elif len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long.")
        
    # Age validation
    if age is None:
        errors.append("Age is required.")
    elif not isinstance(age, int):
        errors.append("Age must be a valid number.")
    elif age <= 0 or age > 120:
        errors.append("Age must be between 1 and 120.")
        
    # Email validation
    if not email or not email.strip():
        errors.append("Email is required.")
    else:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append("Please enter a valid email address.")
            
    # Phone validation
    if not phone or not phone.strip():
        errors.append("Phone number is required.")
    else:
        # Adjust the pattern based on your phone number format requirements
        phone_pattern = r'^\+?1?\d{9,15}$'
        if not re.match(phone_pattern, phone):
            errors.append("Please enter a valid phone number.")
            
    # Password validation
    if not password:
        errors.append("Password is required.")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter.")
    elif not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter.")
    elif not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number.")
        
    # Avatar validation
    if not avatar:
        errors.append("Avatar is required.")
    elif avatar.filename:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if avatar.content_type not in allowed_types:
            errors.append("Avatar must be a JPEG, PNG, or GIF file.")
        
    return errors