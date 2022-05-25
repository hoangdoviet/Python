from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

# from user import UserInDBBase
# Shared properties


# Properties to receive via API on creation


class OrderCreate(BaseModel):
    cart: List[str]


# Properties to receive via API on update
class OrderUpdate(BaseModel):
    discount: Optional[str] = None
    quantity: int = 1
    sum_price: Optional[int] = 0

class OrderInDBBase(BaseModel):
    id: Optional[UUID] = None
    sum_price: Optional[int] = 0

    class Config:
        orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    pass

class UserOrder(BaseModel):
    order: List[Order] = []
    total_price: int = 1

    class Config:
        orm_mode = True



