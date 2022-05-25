from .crud_user import user
from .crud_user_profile import user_profile
from .crud_categories import categories
from .crud_discount import discount
from .crud_product import product
from .crud_cart import cart
from .crud_order import order
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
