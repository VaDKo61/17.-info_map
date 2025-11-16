from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from schemas import BuildingsAndOrganizationsResponse
from services import BuildingService

router = APIRouter(tags=['buildings'])


@router.get(
    '/search_area',
    response_model=BuildingsAndOrganizationsResponse,
    description='Список организаций и список зданий,'
                ' которые находятся в заданном радиусе/прямоугольной области'
)
async def get_buildings_by_area(
        lat: float | None = Query(None),
        lng: float | None = Query(None),
        radius: float | None = Query(None, description='в км'),
        lat_min: float | None = Query(None),
        lat_max: float | None = Query(None),
        lng_min: float | None = Query(None),
        lng_max: float | None = Query(None),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    buildings, organizations = await BuildingService.get_buildings_from_area(
        session=session,
        lat=lat,
        lng=lng,
        radius=radius,
        lat_min=lat_min,
        lat_max=lat_max,
        lng_min=lng_min,
        lng_max=lng_max
    )

    return BuildingsAndOrganizationsResponse(
        buildings=buildings,
        organizations=organizations
    )
