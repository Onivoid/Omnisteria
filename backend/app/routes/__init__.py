from fastapi import APIRouter
from .users import router as users_router
from .characters import router as characters_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(characters_router, prefix="/characters", tags=["Characters"])