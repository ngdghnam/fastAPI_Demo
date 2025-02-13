from database import db
from lightdb.models import Model
# from pydantic import BaseModel
import bcrypt

class User(Model, table="users", db=db):
    name: str
    phone: str
    email: str 
    password: str

    @staticmethod
    def hashPassword(password: str) -> str:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')  # Store as string in database
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Verify a password against its hash
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
