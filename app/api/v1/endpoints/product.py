from typing import Any, List, Union, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.exception_handler import CustomException
from app.models import DbProduct, DbCategories
from app.schemas import Categories
from app.schemas.base import DataResponse

router = APIRouter()


@router.get("", response_model=DataResponse[List[schemas.Product]])
async def read_product(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Retrieve Product.
    """

    product = crud.product.get_multi_by_user(db, skip=skip, limit=limit, user=current_user)

    return DataResponse().success_response(request, product)


@router.post("/open", response_model=DataResponse[schemas.ProductCategories])
def create_product(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        product_in: schemas.ProductCreate,
        category_in: List[str],
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa

) -> Any:
    """
    Create new Product
    """

    category = []
    for item in category_in:
        cat = crud.categories.get_by_user(db, id=item, user_id=current_user.id)
        if not cat:
            raise CustomException(
                http_code=404,
                message="The Categories  does not exist in the system",
            )
        category.append(cat)

    product = crud.product.create(db, obj_in=product_in, user=current_user, cat=category)

    return DataResponse().success_response(request, product)


@router.put("/{product_id}", response_model=DataResponse[schemas.ProductCategories])
def update_product(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        product_id: str,
        product_in: schemas.ProductUpdate,
        category_in: List[str],
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  Product.
    """
    product = crud.product.get_by_user(db, id=product_id, user_id=current_user.id)
    if not product:
        raise CustomException(
            http_code=404,
            message="The Product  does not exist in the system",
        )
    if product.created_by != str(current_user.id):
        raise CustomException(
            http_code=404,
            message="The Product does not exist in the system",
        )
    category = []
    for item in category_in:
        cat = crud.categories.get(db, id=item)
        if not cat:
            raise CustomException(
                http_code=404,
                message="The Categories  does not exist in the system",
            )
        category.append(cat)
    crud.product.create_product_categories(db, product_id=product.id, cat=category)
    product = crud.product.update(db, db_obj=product, obj_in=product_in)
    return DataResponse().success_response(request, product)


@router.get("/{product_id}", response_model=DataResponse[schemas.Product])
def read_product(
        request: Request,
        product_id: str,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Get Product by id.
    """
    current_product = crud.product.get_by_user(db, id=product_id, user_id=current_user.id)
    if not current_product:
        raise CustomException(
            http_code=404,
            message="The Product does not exist in the system",
        )
    return DataResponse().success_response(request, current_product)


@router.get("/{product_id}/categories", response_model=DataResponse[schemas.ProductCategories])
def read_product_categories(
        request: Request,
        product_id: str,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Get Product Categories.
    """
    current_product = crud.product.get_by_user(db, id=product_id, user_id=current_user.id)
    if not current_product:
        raise CustomException(
            http_code=404,
            message="The Product does not exist in the system",
        )
    return DataResponse().success_response(request, current_product)


@router.get("/{product_id}/discount", response_model=DataResponse[schemas.ProductDiscount])
def read_product_discounts(
        request: Request,
        product_id: str,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Get Product Discount.
    """
    current_product = crud.product.get_by_user(db, id=product_id,user_id=current_user.id)
    if current_product.created_by != str(current_user.id):
        raise CustomException(
            http_code=404,
            message="The Product does not exist in the system",
        )
    return DataResponse().success_response(request, current_product)


@router.delete("/{product_id}")
def delete_product(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        product_id: str,

        current_user: models.DbUser = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    """
    Update  Product.
    """
    product = crud.product.get_by_user(db, id=product_id,user_id=current_user.id)
    if not product:
        raise CustomException(
            http_code=404,
            message="The Product does not exist in the system",
        )
    delete = {
        "deleted": True
    }
    product = crud.product.update(db, db_obj=product, obj_in=delete)
    return DataResponse().success_response(request, "Delete Success")
