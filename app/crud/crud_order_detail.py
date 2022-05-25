import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import false, true, and_
from sqlalchemy.orm import Session

from app import crud
from app.core.exception_handler import CustomException
from app.crud.base import CRUDBase
from app.models import DbUser, DbCategories, DbOrderDetail, DbOrderDetailDetail
from app.models.db_OrderDetail import DbOrderDetail
from app.schemas import UserCart
from app.schemas.OrderDetail import OrderDetailCreate, OrderDetailUpdate


class CRUDOrderDetail(CRUDBase[DbOrderDetail, OrderDetailCreate, OrderDetailUpdate]):



order_detail = CRUDOrderDetail(DbOrderDetail)
