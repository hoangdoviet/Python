from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

# Shared properties
from app.schemas import Product, Discount, Order


class OrderDetailBase(BaseModel):
    product: Product
    discount: Optional[Discount] = None
    quantity: int = 0
    sum_price: int = None

class OrderDetailInDBBase(OrderDetailBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class OrderDetail(OrderDetailInDBBase):
    pass

class UserOrderDetail(Order):
    order_detail: List[OrderDetail] = []

