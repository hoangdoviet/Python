import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import DbUser, DbCategories
from app.models.db_product import DbProduct
from app.models.db_product_categories import DbProductCategories
from app.schemas.product import ProductUpdate, ProductCreate, ProductDelete


class CRUDProduct(CRUDBase[DbProduct, ProductCreate, ProductUpdate]):

    def create(self, db: Session, *, obj_in: ProductCreate, user: DbUser, cat: List[DbCategories]) -> DbProduct:

        db_obj = DbProduct(
            name=obj_in.name,
            price=obj_in.price,
            created_by=user.id,
            updated_by=user.id,
            quantity=obj_in.quantity,
            categories=cat
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: DbProduct, obj_in: Union[ProductUpdate, Dict[str, Any]]
    ) -> DbProduct:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_name(self, db: Session, *, name: str) -> Optional[DbProduct]:
        return db.query(DbProduct).filter(DbProduct.name == name) \
            .filter(DbProduct.deleted == "false").first()

    def create_product_categories(
            self, db: Session, *,  product_id: uuid,
            cat: List[DbCategories]
    ) -> DbProductCategories:
        for item in db.query(DbProductCategories).filter(DbProductCategories.product_id == product_id):
            db.delete(item)
            db.commit()
        for item in cat:
            db_obj = DbProductCategories(
                product_id=product_id,
                category_id=item.id
            )
            db.add(db_obj)
            db.commit()
        return

    def delete(
            self, db: Session, *, db_obj: DbProduct, obj_in: Union[ProductDelete, Dict[str, Any]]
    ) -> DbProduct:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def get_product_categories(self, db: Session, *, product_id: Any) -> List[DbCategories]:
    #     categories = db.query(DbProductCategories).filter(DbProductCategories.product_id == product_id) \
    #                                             .filter(DbProductCategories.deleted == "false").all()
    #     product_categories = []
    #     for item in categories:
    #         product_categories.append(crud.categories.get(db, id=item.id))
    #     return


product = CRUDProduct(DbProduct)
