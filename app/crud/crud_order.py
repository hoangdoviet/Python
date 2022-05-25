import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true, and_
from sqlalchemy.orm import Session

from app import crud
from app.core.exception_handler import CustomException
from app.crud.base import CRUDBase
from app.models import DbUser, DbCategories, DbOrder, DbOrderDetail
from app.models.db_order import DbOrder
from app.schemas import UserCart, ProductUpdate
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[DbOrder, OrderCreate, OrderUpdate]):
    def get_last_order(
            self, db: Session, *, skip: int = 0, limit: int = 0, user_id: Any
    ) -> List[DbOrder]:

        return db.query(DbOrder).filter(and_(DbOrder.deleted == "false", DbOrder.created_by == str(user_id)))\
            .order_by(DbOrder.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: OrderCreate, user: DbUser) -> DbOrder:
        user_cart = crud.cart.get_list_cart(db, obj_in=obj_in, user=user)
        if not user_cart:
            raise CustomException(
                http_code=404,
                message="Pls, choose some product to order"
            )


        db_obj = DbOrder(
            user_id=user.id,
            created_by=user.id,
            sum_price=user_cart.total_price
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        db_obj.order_detail = []
        for item in user_cart.cart:
            discount = None
            if item.discount:
                discount = item.discount.id
            order_detail = DbOrderDetail(
                created_by=user.id,
                order_id=db_obj.id,
                product_id=item.product.id,
                discount_id=discount,
                quantity=item.quantity,
                sum_price=item.sum_price
            )
            product = crud.product.get(db, id=item.product.id)
            quantity = {
                "quantity": product.quantity - item.quantity
            }
            crud.product.update(db, db_obj=product, obj_in=quantity)

            db.add(order_detail)
            db_obj.order_detail.append(order_detail)
        db.commit()
        db.refresh(order_detail)

        return db_obj

    def update(
            self, db: Session, *, db_obj: DbOrder, obj_in: Union[OrderUpdate, Dict[str, Any]]
    ) -> DbOrder:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


order = CRUDOrder(DbOrder)
