from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbProductDiscount(BaseModel):
    product_id = Column(UUID(as_uuid=True), ForeignKey('db_product.id'), primary_key=True)
    discount_id = Column(UUID(as_uuid=True), ForeignKey('db_discount.id'), primary_key=True)
