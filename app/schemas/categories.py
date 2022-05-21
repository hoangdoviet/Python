from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel
# from user import UserInDBBase
# Shared properties
from app import schemas


class CategoriesBase(BaseModel):

    name: Optional[str] = None

# Properties to receive via API on creation
class CategoriesCreate(CategoriesBase):
    name: str


# Properties to receive via API on update
class CategoriesUpdate(CategoriesBase):
    name: Optional[str] = None

class CategoriesDelete(CategoriesBase):
    deleted: bool

class CategoriesInDBBase(CategoriesBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True



# Additional properties to return via API
class Categories(CategoriesInDBBase):
    pass
#
# class Test:
#     cate_list = List[Categories],
#     user_data = UserInDBBase
