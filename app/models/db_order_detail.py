from sqlalchemy import Column,  INTEGER,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbOrderDetail(BaseModel):
    order_id = Column(UUID(as_uuid=True), ForeignKey("db_order.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("db_product.id"))
    discount_id = Column(UUID(as_uuid=True), ForeignKey("db_discount.id"))
    quantity = Column(INTEGER, index=True)
    sum_price = Column(INTEGER, index=True)
    product = relationship("DbProduct", back_populates="order_detail")
    order = relationship("DbOrder", back_populates="order_detail")
    discount = relationship("DbDiscount", back_populates="order_detail")


