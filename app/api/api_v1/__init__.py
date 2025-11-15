from fastapi import APIRouter

from core.config import settings

from .organization import router as organization_router
from .building import router as buildings_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(
    organization_router,
    prefix=settings.api.v1.organizations,
)

router.include_router(
    buildings_router,
    prefix=settings.api.v1.buildings
)
