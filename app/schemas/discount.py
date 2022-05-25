from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

# Shared properties

class DiscountBase(BaseModel):
    code: Optional[str] = None
    discount: Optional[int] = 10

# Properties to receive via API on creation
class DiscountCreate(DiscountBase):
    code: str
    discount = int


# Properties to receive via API on update
class DiscountUpdate(DiscountBase):
    code: str
    discount = int

class DiscountDelete(DiscountBase):
    deleted: bool

class DiscountInDBBase(DiscountBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Discount(DiscountInDBBase):
    pass
#
# class Test:
#     cate_list = List[Discount],
#     user_data = UserInDBBase
