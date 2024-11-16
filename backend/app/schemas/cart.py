from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional

class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    cart_id: int

    class Config:
        from_attributes = True

class CartBase(BaseModel):
    user_id: int
    total_amount: Decimal = Decimal(0)

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    items: List[CartItem] = []

    class Config:
        from_attributes = True
