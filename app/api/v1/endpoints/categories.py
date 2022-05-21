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


@router.get("", response_model=DataResponse[List[schemas.Categories]])
def read_categories(
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Retrieve Discount.
    """

    categories = crud.categories.get_multi(db, skip=skip, limit=limit)

    return DataResponse().success_response(request, categories)


@router.post("/open", response_model=DataResponse[schemas.Categories])
def create_category(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        category_in: schemas.CategoriesCreate,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa

) -> Any:
    """
    Create new Category.
    """
    exist_category = crud.categories.get_by_name(db, name=category_in.name)
    if exist_category:
        raise CustomException(http_code=status.HTTP_400_BAD_REQUEST,
                              message="The Category already exists in the system.")

    category = crud.categories.create(db, obj_in=category_in)

    return DataResponse().success_response(request, category)


@router.put("/{cat_id}", response_model=DataResponse[schemas.Categories])
def update_cat(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        category_id: str,
        category_in: schemas.CategoriesUpdate,
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update  category.
    """
    cat = crud.categories.get(db, id=category_id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The Categories  does not exist in the system",
        )
    exist_cat = crud.categories.get_by_name(db, name=category_in.name)
    if exist_cat:
        raise CustomException(
            http_code=404,
            message="The Category already exists in the system.",
        )
    category = crud.categories.update(db, db_obj=cat, obj_in=category_in)
    return DataResponse().success_response(request, category)


@router.get("/{cat_id}", response_model=DataResponse[schemas.Categories])
def read_cat(
        request: Request,
        category_id: str,
        db: Session = Depends(deps.get_db),  # noqa
        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Get cat by id.
    """
    current_cat = crud.categories.get(db, id=category_id)
    return DataResponse().success_response(request, current_cat)


@router.delete("/{cat_id}")
def delete_cat(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        category_id: str,

        current_user: models.DbUser = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update  category.
    """
    cat = crud.categories.get(db, id=category_id)
    if not cat:
        raise CustomException(
            http_code=404,
            message="The Categories does not exist in the system",
        )
    delete = {
        "deleted": True
    }
    category = crud.categories.update(db, db_obj=cat, obj_in=delete)

    return DataResponse().success_response(request, "Delete Success")
