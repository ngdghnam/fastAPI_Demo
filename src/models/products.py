from pydantic import BaseModel

class Products(BaseModel):
    """
    Trường dữ liệu Products 
    """
    name: str
    description: str
    price: int  