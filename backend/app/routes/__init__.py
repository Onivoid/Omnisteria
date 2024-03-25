from fastapi import APIRouter

from .hw import router as hw_router
from .ingredients import router as ingredients_router
from .users import router as users_router

router = APIRouter()

router.include_router(hw_router, tags=["HelloWorld"])
router.include_router(ingredients_router, prefix="/ingredients", tags=["Ingredients"])
router.include_router(users_router, prefix="/users", tags=["Users"])