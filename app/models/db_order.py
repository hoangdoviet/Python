from sqlalchemy import Column,  INTEGER,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DbOrder(BaseModel):
    user_id = Column(UUID(as_uuid=True), ForeignKey("db_user.id"))
    sum_price = Column(INTEGER, index=True)
    user = relationship("DbUser", back_populates="order")
    order_detail = relationship("DbOrderDetail", back_populates="order")



