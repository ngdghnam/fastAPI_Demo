from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str 
    age: int 
    phone: str
    email: str
    password: str 
    avatar: str 
    # images: List[str]