from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from schemas import BuildingOrganizationsResponse, ActivityOrganizationsResponse, OrganizationWithBuilding
from services import OrganizationService

router = APIRouter(tags=['organizations'])


@router.get(
    '',
    response_model=list[OrganizationWithBuilding]
)
async def get_organizations(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_organizations(
        session
    )
    return organizations


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


@router.get(
    '/by-activity/search',
    response_model=list[OrganizationWithBuilding]
)
async def search_organizations_by_activity(
        name: str = Query(..., description="Название вида деятельности, например 'Еда'"),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_by_activity_name(
        name=name,
        session=session
    )
    return organizations


@router.get(
    '/by-activity/{activity_id}',
    response_model=ActivityOrganizationsResponse
)
async def get_organizations_by_activity(
        activity_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_organizations_by_activity(
        activity_id,
        session
    )
    return ActivityOrganizationsResponse(
        activity_id=activity_id,
        organizations=organizations
    )


