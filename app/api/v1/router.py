from fastapi import APIRouter

from app.api.v1.endpoints import (status, authen, users, categories, discount, product, cart, order)

api_router = APIRouter()
api_router.include_router(status.router, tags=["StarterAPI"])
api_router.include_router(authen.router, tags=["Authen"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router(categories.router, prefix="/category", tags=["Categories"])
api_router.include_router(discount.router, prefix="/discount", tags=["Discount"])
api_router.include_router(product.router, prefix="/product", tags=["Product"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(order.router, prefix="/order", tags=["Order"])



