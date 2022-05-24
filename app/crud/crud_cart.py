import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true, and_
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import DbUser, DbCategories, DbCart
from app.models.db_cart import DbCart
from app.schemas.cart import CartUpdate, CartCreate, CartDelete


class CRUDCart(CRUDBase[DbCart, CartCreate, CartUpdate]):

    def get_cart(self, db: Session, id: Any, product_id: Any) -> Optional[DbCart]:
        return db.query(DbCart).filter(and_(DbCart.user_id == id, DbCart.product_id == product_id)).all()

    def create(self, db: Session, *, obj_in: CartCreate, user: DbUser) -> DbCart:
        print(user.id)
        print(obj_in.discount)
        db_obj = DbCart(
            user_id=user.id,
            product_id=obj_in.product,
            discount=obj_in.discount,
            quantity=obj_in.quantity
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
        print(db_obj.name)
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
