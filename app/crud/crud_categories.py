from typing import Any, Dict, Optional, Union

from sqlalchemy import false, true
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.db_categories import DbCategories
from app.schemas.categories import CategoriesUpdate, CategoriesCreate, CategoriesDelete


class CRUDCategories(CRUDBase[DbCategories, CategoriesCreate, CategoriesUpdate]):

    def create(self, db: Session, *, obj_in: CategoriesUpdate) -> DbCategories:
        db_obj = DbCategories(
            name=obj_in.name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: DbCategories, obj_in: Union[CategoriesUpdate, Dict[str, Any]]
    ) -> DbCategories:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_name(self, db: Session, *, name: str) -> Optional[DbCategories]:
        return db.query(DbCategories).filter(DbCategories.name == name)\
            .filter(DbCategories.deleted == "false").first()

    def delete(
            self, db: Session, *, db_obj: DbCategories, obj_in: Union[CategoriesDelete, Dict[str, Any]]
    ) -> DbCategories:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


categories = CRUDCategories(DbCategories)
