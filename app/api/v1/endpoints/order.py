import math
import uuid
from operator import concat
from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas import Product, Discount
from app.schemas.base import DataResponse

router = APIRouter()

@router.get("", response_model=DataResponse[List[schemas.UserOrderDetail]])
def read_order(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Retrieve Discount.
    """

    order = crud.order.get_multi_by_user(db, skip=skip, limit=limit, user=current_user)
    if not order:
        raise CustomException(
            http_code=404,
            message="%s dont have any order" % current_user.username
        )

    return DataResponse().success_response(request, order)


@router.post("/open", response_model=DataResponse[schemas.UserOrderDetail])
def create_order(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        order_in: List[str],
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Create new order.
    """
    order = crud.order.create(db, obj_in=order_in, user=current_user)
    for item in order_in:
        crud.cart.remove(db, id=item)
    return DataResponse().success_response(request, order)



@router.delete("/{order_id}")
def delete_order(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        order_id: str,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Delete  order.
    """
    cat = crud.order.get_by_user(db, id=order_id, user_id=current_user.id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The order does not exist in the system",
        )
    delete = {
        "deleted": True
    }
    crud.order.update(db, db_obj=cat, obj_in=delete)

    return DataResponse().success_response(request, "Delete Success")



