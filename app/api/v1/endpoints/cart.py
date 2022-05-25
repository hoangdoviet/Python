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

def sum_price(product: int, discount: int, quantity: int):
    total = product * quantity * (1-discount/100)
    return math.ceil(total)

@router.get("", response_model=DataResponse[schemas.UserCart])
def read_cart(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Retrieve Discount.
    """

    cart = crud.cart.get_multi_by_user(db, skip=skip, limit=limit, user=current_user)

    new_cart = schemas.UserCart
    new_cart.cart = cart
    price = 0
    for item in cart:
        price += item.sum_price
    new_cart.total_price = price
    last_order = crud.order.get_last_order(db, user_id=current_user.id, limit=2)
    print(last_order)
    new_cart.last_order = last_order
    return DataResponse().success_response(request, new_cart)


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
    print(cart_in.product_id)
    product = crud.product.get(db, id=cart_in.product_id)
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
    discount = 0
    print(cart_in.discount_id)
    if cart_in.discount_id:
        discount_id = None
        for item in product.discount:
            if item.code == cart_in.discount_id:
                discount_id = item.id
                discount = item.discount

        if not discount_id:
            raise CustomException(
                http_code=404,
                message="Dont Have Discount Code Like This",
            )
        cart_in.discount_id = discount_id

    else:
        cart_in.discount_id = None
    cart_in.product_id = product.id

    exist_product = crud.cart.get_cart_product(db, id=current_user.id, product_id=cart_in.product_id)

    if exist_product:
        # update product//
        cart_in.quantity += exist_product.quantity
        if product.quantity < cart_in.quantity:
            raise CustomException(
                http_code=404,
                message="The %s not enough in the system, just have %d" % (product.name, product.quantity)
            )
        total = sum_price(product=product.price, discount=discount, quantity=cart_in.quantity)
        cart_in.sum_price = total
        cart = crud.cart.update(db, db_obj=exist_product, obj_in=cart_in)
    else:
        total = sum_price(product=product.price, discount=discount, quantity=cart_in.quantity)
        cart = crud.cart.create(db, obj_in=cart_in, user=current_user, total=total)

    return DataResponse().success_response(request, cart)


@router.put("/{cat_id}", response_model=DataResponse[schemas.Cart])
def update_cart(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        cart_id: str,
        cart_in: schemas.CartUpdate,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  cart.
    """
    cat = crud.cart.get_by_user(db, id=cart_id, user_id=current_user.id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The %s  does not exist any cart in the system" % current_user.username
        )
    discount = 0
    if cart_in.discount_id:
        discount_id = None
        for item in cat.product.discount:
            if item.code == cart_in.discount_id:
                discount_id = item.id
                discount = item.discount
        if not discount_id:
            raise CustomException(
                http_code=404,
                message="Dont Have Discount Code Like This",
            )
        cart_in.discount_id = discount_id
    else:
        cart_in.discount_id = None

    total = sum_price(product=cat.product.price, discount=discount, quantity=cart_in.quantity)
    cart_in.sum_price = total
    cart = crud.cart.update(db, db_obj=cat, obj_in=cart_in)
    return DataResponse().success_response(request, cart)


@router.delete("/{cart_id}")
def delete_cart(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        cart_id: str,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  cart.
    """
    cat = crud.cart.get_by_user(db, id=cart_id, user_id=current_user.id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The cart does not exist in the system",
        )
    crud.cart.remove(db, id=cat.id)

    return DataResponse().success_response(request, "Delete Success")



