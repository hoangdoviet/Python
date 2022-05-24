from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
# from user import UserInDBBase
# Shared properties


class CartBase(BaseModel):
    product: str


# Properties to receive via API on creation
class CartCreate(CartBase):
    product: str
    discount: Optional[str] = None
    quantity: int = 1



# Properties to receive via API on update
class CartUpdate(CartBase):
    product: str
    discount: Optional[str] = None
    quantity: int = 1


class CartDelete(CartBase):
    deleted: bool


class CartInDBBase(CartBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cart(CartInDBBase):
    pass
