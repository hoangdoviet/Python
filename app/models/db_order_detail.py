from sqlalchemy import Column,  INTEGER,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbOrderDetail(BaseModel):
    order_id = Column(UUID(as_uuid=True), ForeignKey("db_order.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("db_product.id"))
    product = relationship("DbProduct", back_populates="order_detail")
    order = relationship("DbOrder", back_populates="order_detail")


