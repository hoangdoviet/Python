import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import DbProduct, DbProductDiscount
from app.models.db_user import DbUser
from app.models.db_discount import DbDiscount
from app.schemas.discount import DiscountUpdate, DiscountCreate, DiscountDelete


class CRUDDiscount(CRUDBase[DbDiscount, DiscountCreate, DiscountUpdate]):

    def create(self, db: Session, *, obj_in: DiscountCreate, user: DbUser, cat: List[DbProduct]) -> DbDiscount:

        db_obj = DbDiscount(
            code=obj_in.code,
            discount=obj_in.discount,
            created_by=user.id,
            updated_by=user.id,
            product=cat
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: DbDiscount, obj_in: Union[DiscountUpdate, Dict[str, Any]]
    ) -> DbDiscount:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        print(db_obj.code)
        print(update_data)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def create_product_discount(
            self, db: Session, *,  discount: uuid,
            cat: List[DbProduct]
    ) -> DbProductDiscount:
        for item in db.query(DbProductDiscount).filter(DbProductDiscount.discount_id == discount):
            db.delete(item)
            db.commit()
        for item in cat:
            db_obj = DbProductDiscount(
                product_id=item.id,
                discount_id=discount
            )
            db.add(db_obj)
            db.commit()
        return

    def get_by_code(self, db: Session, *, code: str, user: DbUser) -> Optional[DbDiscount]:
        return db.query(DbDiscount).filter(DbDiscount.code == code)\
                                    .filter(DbDiscount.deleted == "false")\
                                    .filter(DbDiscount.created_by == str(user.id)).first()

    def delete(
            self, db: Session, *, db_obj: DbDiscount, obj_in: Union[DiscountDelete, Dict[str, Any]]
    ) -> DbDiscount:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


discount = CRUDDiscount(DbDiscount)
