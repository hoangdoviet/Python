from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models import DbUser
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).filter(self.model.deleted == "false").first()

    def get_by_user(self, db: Session, id: Any, user_id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).filter(and_(self.model.deleted == "false")
                                                                       , self.model.created_by == str(user_id)).first()

    def get_with_product_by_user(self, db: Session, id: Any, userid: Any) -> Optional[ModelType]:
        t = db.query(self.model).filter(and_(self.model.id == id, self.model.deleted == "false",
                                             self.model.created_by == str(userid))).first()
        if t:
            if t.product:
                for item in t.product:
                    if item.created_by != str(userid):
                        t.product.remove(item)
        return t

    # db.query(self.model).filter(and_(self.model.id == id, self.model.deleted == "false",
    #                                  self.model.product.id == userid)).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).filter(self.model.deleted == "false").offset(skip).limit(limit).all()

    def get_multi_by_user(
            self, db: Session, *, skip: int = 0, limit: int = 100, user: DbUser
    ) -> List[ModelType]:
        return db.query(self.model).filter(self.model.deleted == "false")\
            .filter(self.model.created_by == str(user.id)) \
            .offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
