from pydantic import BaseModel
import datetime
from typing import List

class Emails(BaseModel):
    studentEmail: str
    personaEmail: str

class Members(BaseModel):
    fullName: str 
    DOB: datetime.date
    school: str  
    faculty: str 
    className: str 
    studentID: str 
    email: Emails
    phone: str 
    department: str 
    role: str
    userName: str 
    password: str 
    images: List[str]

