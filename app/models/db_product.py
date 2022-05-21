from sqlalchemy import Column, String, INTEGER, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel

class DbProduct(BaseModel):
    name = Column(String, index=True)
    price = Column(INTEGER, index=True)
    quantity = Column(INTEGER, index=True)
    is_active = Column(Boolean(), default=True)
    categories = relationship("DbCategories", secondary='db_product_categories', back_populates="product")
    discount = relationship('DbDiscount', secondary='db_product_discount', back_populates="product")
    cart = relationship("DbCart", back_populates="product")
    order_detail = relationship("DbOrderDetail", back_populates="product")



