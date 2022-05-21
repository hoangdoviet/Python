from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel
from app import schemas

# Shared properties
from app.models import DbCategories
from app.schemas import Categories, Discount


class ProductBase(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = 0
    quantity: Optional[int] = 1

# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    price: Optional[int] = 0
    quantity: Optional[int] = 1


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[int] = 0
    quantity: Optional[int] = 1
    categories: List[Categories] = []


class ProductDelete(ProductBase):
    deleted: bool


class ProductInDBBase(ProductBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


class ProductCategories(ProductInDBBase):
    categories: List[Categories] = []


class ProductDiscount(ProductInDBBase):
    discount: List[Discount] = []


# Additional properties to return via API
class Product(ProductInDBBase):
    pass

#
# class Test:
#     cate_list = List[Categories],
#     user_data = UserInDBBase
