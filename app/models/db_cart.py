from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbCart(BaseModel):
    user_id = Column(UUID(as_uuid=True), ForeignKey("db_user.id"), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("db_product.id"))
    user = relationship("DbUser", back_populates="cart")
    product = relationship("DbProduct", back_populates="cart")


