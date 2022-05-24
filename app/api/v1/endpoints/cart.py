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
from app.schemas.base import DataResponse

router = APIRouter()


@router.get("", response_model=DataResponse[List[schemas.Cart]])
def read_cart(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve Discount.
    """

    cart = crud.cart.get_multi(db, skip=skip, limit=limit)

    return DataResponse().success_response(request, cart)


@router.post("/open", response_model=DataResponse[schemas.Cart])
def create_cart(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        cart_in: schemas.CartCreate,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Create new cart.
    """
    product = crud.product.get(db, id=cart_in.product)
    if not product:
        raise CustomException(
            http_code=404,
            message="The Product not exist in the system"
        )
    if product.quantity < cart_in.quantity:
        raise CustomException(
            http_code=404,
            message="The %s not enough in the system, just have %d" % (product.name, product.quantity)
        )
    discount = None
    for item in product.discount:
        if item.code == cart_in.discount:
            discount = item.id
    if not discount:
        raise CustomException(
            http_code=404,
            message="Dont Have Discount Code",
        )

    cart_in.discount = discount
    exist_product = crud.cart.get_cart(db, id=current_user.id, product_id=cart_in.product)
    if exist_product:
        # update product//
        cart = crud.cart.update(db, db_obj=exist_product, obj_in=cart_in)
    else:
        cart = crud.cart.create(db, obj_in=cart_in, user=current_user)

    return DataResponse().success_response(request, cart)


@router.put("/{cat_id}", response_model=DataResponse[schemas.Cart])
def update_cat(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        cart_id: str,
        cart_in: schemas.CartUpdate,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update  cart.
    """
    cat = crud.cart.get(db, id=cart_id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The cart  does not exist in the system",
        )
    exist_cat = crud.cart.get_by_name(db, name=cart_in.name)
    if exist_cat:
        raise CustomException(
            http_code=404,
            message="The cart already exists in the system.",
        )
    cart = crud.cart.update(db, db_obj=cat, obj_in=cart_in)
    return DataResponse().success_response(request, cart)


@router.delete("/me")
def delete_cat(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        cart_id: str,

        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  cart.
    """
    cat = crud.cart.get_cart(db, id=current_user.id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The cart does not exist in the system",
        )
    delete = {
        "deleted": True
    }
    cart = crud.cart.update(db, db_obj=cat, obj_in=delete)

    return DataResponse().success_response(request, "Delete Success")
