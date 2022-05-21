from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbProductCategories(BaseModel):
    product_id = Column(UUID(as_uuid=True), ForeignKey('db_product.id'), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('db_categories.id'), primary_key=True)
