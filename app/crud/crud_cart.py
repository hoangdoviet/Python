import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true, and_
from sqlalchemy.orm import Session

from app import crud
from app.core.exception_handler import CustomException
from app.crud.base import CRUDBase
from app.models import DbUser, DbCategories, DbCart
from app.models.db_cart import DbCart
from app.schemas.cart import CartUpdate, CartCreate, CartDelete, UserCart, Cart


class CRUDCart(CRUDBase[DbCart, CartCreate, CartUpdate]):

    def get_cart_product(self, db: Session, id: Any, product_id: Any) -> Optional[DbCart]:
        return db.query(DbCart).filter(and_(DbCart.user_id == id, DbCart.product_id == product_id, DbCart.deleted == "false")).first()

    def get_list_cart(self, db: Session, obj_in: List[str], user: DbUser) -> UserCart:
        user_cart = UserCart
        total = 0
        list_cart = []
        for item in obj_in:

            c = crud.cart.get_by_user(db, user_id=user.id, id=item)
            if not c:
                raise CustomException(
                    http_code=404,
                    message="You dont have this cart"
                )

            list_cart.append(c)
            total += c.sum_price
        user_cart.cart = list_cart
        user_cart.total_price = total
        return user_cart

    def create(self, db: Session, *, obj_in: CartCreate, user: DbUser, total:int) -> Optional[UserCart]:

        db_obj = DbCart(
            user_id=user.id,
            created_by=user.id,
            product_id=obj_in.product_id,
            discount_id=obj_in.discount_id,
            quantity=obj_in.quantity,
            sum_price=total
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: DbCart, obj_in: Union[CartUpdate, Dict[str, Any]]
    ) -> DbCart:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(
            self, db: Session, *, db_obj: DbCart, obj_in: Union[CartDelete, Dict[str, Any]]
    ) -> DbCart:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


cart = CRUDCart(DbCart)
