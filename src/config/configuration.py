# from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Đối với python, chúng ta sẽ không thể làm việc trực tiếp với file .env 
    như javascript. Vì thế phải cấu hình 1 class có các biến trùng với 
    các biến môi trường trong file .env
    """
    DB_URL: str
    PORT: str 
    JWT_SECRET_KEY: str 
    TOKEN_LIFETIME: str 
    REFRESH_TOKEN_KEY: str 
    REFRESH_TOKEN_LIVETIME: str 

    class Config:
        env_file = ".env"

settings = Settings()