from sqlalchemy import Boolean, Column, Integer, String, Numeric
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(10, 2))
    stock = Column(Integer)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
