from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

# from user import UserInDBBase
# Shared properties
from app.schemas import Product, Discount


class CartBase(BaseModel):
    quantity: int


# Properties to receive via API on creation
class CartCreate(CartBase):
    product: str
    discount: Optional[str] = None
    quantity: int = 1
    sum_price: Optional[int] = 0


# Properties to receive via API on update
class CartUpdate(CartBase):
    discount: Optional[str] = None
    quantity: int = 1
    sum_price: Optional[int] = 0

class CartDelete(CartBase):
    deleted: bool


class CartInDBBase(CartBase):
    id: Optional[UUID] = None
    product: Product
    discount: Optional[Discount] = None
    sum_price: Optional[int] = 0

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cart(CartInDBBase):
    pass

class UserCart(BaseModel):
    cart: List[Cart] = []
    total_price: int = 1

    class Config:
        orm_mode = True

class CartInfo(Cart):
    id: Optional[UUID] = None
    product: List[Product] = None
    discount: List[Discount] = None
