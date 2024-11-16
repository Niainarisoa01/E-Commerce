from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    total_amount: Decimal
    status: str = "pending"  # pending, completed, cancelled

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True
