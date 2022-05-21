from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class DbCategories(BaseModel):
    name = Column(String, index=True)
    product = relationship('DbProduct', secondary='db_product_categories', back_populates="categories")
