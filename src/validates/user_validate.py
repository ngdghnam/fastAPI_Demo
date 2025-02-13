from fastapi import Form, HTTPException
from typing import List


async def validate_user_input(
    name: str = Form(...), 
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
) -> dict:
    errors: List[str] = []

    if not name:
        errors.append("Name is required.")
    if not phone:
        errors.append("Phone is required.")
    if not email:
        errors.append("Email is required.")
    if not phone:
        errors.append("Password is required.")

    if errors:
        return {"errors": errors, "name": name, "phone": phone,  "email": email, "password": password}

    print({"name": name, "phone": phone,"email": email, "password": password})

    return {"name": name, "phone": phone,"email": email, "password": password}
