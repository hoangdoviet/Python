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


@router.get("", response_model=DataResponse[List[schemas.Discount]])
def read_discount(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Retrieve Discount.
    """

    discount = crud.discount.get_multi_by_user(db, skip=skip, limit=limit, user=current_user)
    if not discount:
        raise CustomException(
            http_code=404,
            message="The Discount already exists in the system.",
        )
    return DataResponse().success_response(request, discount)


@router.post("/open", response_model=DataResponse[schemas.DiscountProduct])
def create_discount(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        discount_in: schemas.DiscountCreate,
        products: List[str],
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Create new Discount
    """
    exist_discount = crud.discount.get_by_code(db, code=discount_in.code, user=current_user)
    if exist_discount:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST,
                              message="The discount already exists in the system.")
    product = []
    for item in products:
        cat = crud.product.get_by_user(db, id=item, user_id=current_user.id)
        if not cat:
            raise CustomException(
                http_code=404,
                message="The Product  does not exist in the system",
            )
        product.append(cat)
    discount = crud.discount.create(db, obj_in=discount_in, user=current_user, cat=product)

    return DataResponse().success_response(request, discount)


@router.put("/{discount_id}", response_model=DataResponse[schemas.DiscountProduct])
def update_discount(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        discount_id: str,
        discount_in: schemas.DiscountUpdate,
        products: List[str],
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  discount.
    """
    discount = crud.discount.get(db, id=discount_id)
    if not discount:
        raise CustomException(
            http_code=404,
            message="The Discount  does not exist in the system",
        )
    exist_discount = crud.discount.get_by_code(db, code=discount_in.code, user=current_user)
    if exist_discount:
        raise CustomException(
            http_code=404,
            message="The discount already exists in the system.",
        )
    product = []
    for item in products:
        cat = crud.product.get_by_user(db, id=item, user_id=current_user.id)
        if not cat:
            raise CustomException(
                http_code=404,
                message="The Product  does not exist in the system",
            )
        product.append(cat)
    crud.discount.create_product_discount(db, discount=discount.id, cat=product)  # đây ạ, em để False vào đây rồi
    discount = crud.discount.update(db, db_obj=discount, obj_in=discount_in)
    return DataResponse().success_response(request, discount)


@router.get("/{discount_id}", response_model=DataResponse[schemas.DiscountProduct])
def read_discount(
        request: Request,
        discount_id: str,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Get discount by id.
    """
    current_discount = crud.discount.get_with_product_by_user(db, id=discount_id, userid=current_user.id)
    if not current_discount:
        raise CustomException(
            http_code=404,
            message="The Discount does not exists in the system.",
        )
    return DataResponse().success_response(request, current_discount)


@router.delete("/{discount_id}")
def delete_discount(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        discount_id: str,

        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  Discount.
    """
    discount = crud.discount.get(db, id=discount_id)
    if not discount:
        raise CustomException(
            http_code=404,
            message="The Discount does not exist in the system",
        )
    delete = {
        "deleted": True
    }
    discount = crud.discount.update(db, db_obj=discount, obj_in=delete)
    print(discount.deleted)
    return DataResponse().success_response(request, "Delete Success")
