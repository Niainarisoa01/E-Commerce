from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True
