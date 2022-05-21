from sqlalchemy import Boolean, Column, String, INTEGER
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class DbDiscount(BaseModel):
    code = Column(String, index=True)
    discount = Column(INTEGER, index=True)
    product = relationship('DbProduct', secondary='db_product_discount', back_populates="discount")
