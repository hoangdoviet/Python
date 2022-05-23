from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
# from user import UserInDBBase
# Shared properties
from app.schemas import Product


class CartBase(BaseModel):
    total_price: int = 0
# Properties to receive via API on creation

# Properties to receive via API on update
class CartUpdate(CartBase):
    name: Optional[str] = None

class CartDelete(CartBase):
    deleted: bool

class CartInDBBase(CartBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True



# Additional properties to return via API
class Cart(CartInDBBase):
    pass
