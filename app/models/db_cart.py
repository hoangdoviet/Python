from sqlalchemy import Column, ForeignKey, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbCart(BaseModel):
    user_id = Column(UUID(as_uuid=True), ForeignKey("db_user.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("db_product.id"))
    quantity = Column(INTEGER, index=True)
    discount_id = Column(UUID(as_uuid=True), ForeignKey("db_discount.id"))
    sum_price = Column(INTEGER, index=True)

    user = relationship("DbUser", back_populates="cart")

    product = relationship("DbProduct", back_populates="cart")
    discount = relationship("DbDiscount", back_populates="cart")



