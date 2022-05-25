from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

from app.schemas import Discount, Product, Categories


class DiscountProduct(Discount):
    product: List[Product] = []

class CategoryProduct(Categories):
    product: List[Product] = []

