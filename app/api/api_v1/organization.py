from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from schemas import BuildingOrganizationsResponse
from services import OrganizationService

router = APIRouter(tags=['organizations'])


@router.get(
    '/by-building/{building_id}',
    response_model=BuildingOrganizationsResponse
)
async def get_organizations_by_building(
        building_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_organizations_in_building(
        building_id,
        session
    )

    return BuildingOrganizationsResponse(
        building_id=building_id,
        organizations=organizations
    )
