from core.database import db_helper
from fastapi import APIRouter, Depends, Query
from schemas import (
    ActivityOrganizationsResponse,
    BuildingOrganizationsResponse,
    OrganizationWithBuilding,
)
from schemas.organization import OrganizationPaginatedResponse, OrganizationRead
from services import OrganizationService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["organizations"])


@router.get(
    "/",
    response_model=OrganizationPaginatedResponse,
    description="Вывод всех организаций",
)
async def get_all_organizations(
    session: AsyncSession = Depends(db_helper.session_getter),
    skip: int = Query(
        0,
        ge=0,
        description="Количество записей для пропуска",
    ),
    limit: int = Query(
        10,
        ge=0,
        description="Максимальное количество записей",
    ),
):
    organizations, total = await OrganizationService.get_all_organizations(
        session=session,
        skip=skip,
        limit=limit,
    )

    page = skip // limit if limit > 0 else 0
    page_count = 1 if limit == 0 else (total + limit - 1) // limit

    return OrganizationPaginatedResponse(
        items=[OrganizationRead.model_validate(i) for i in organizations],
        total=total,
        page=page,
        page_size=limit,
        page_count=page_count,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationWithBuilding,
    description="Вывод информации об организации по её идентификатору",
)
async def get_organizations(
    organization_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_by_organization_id(
        organization_id,
        session,
    )
    return organizations


@router.get(
    "/by-building/{building_id}",
    response_model=BuildingOrganizationsResponse,
    description="Список всех организаций находящихся в конкретном здании",
)
async def get_organizations_by_building(
    building_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_organizations_in_building(
        building_id, session
    )

    return BuildingOrganizationsResponse(
        building_id=building_id, organizations=organizations
    )


@router.get(
    "/by-activity/search",
    response_model=list[OrganizationWithBuilding],
    description="Поиск организации по виду деятельности",
)
async def search_organizations_by_activity(
    name: str = Query(..., description="Название вида деятельности, например 'Еда'"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    organizations = await OrganizationService.get_by_activity_name(
        name=name, session=session
    )
    return organizations


@router.get(
    "/by-activity/{activity_id}",
    response_model=ActivityOrganizationsResponse,
    description="Список организаций по виду деятельности",
)
async def get_organizations_by_activity(
    activity_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.get_organizations_by_activity(
        activity_id, session
    )
    return ActivityOrganizationsResponse(
        activity_id=activity_id, organizations=organizations
    )


@router.get(
    "/search",
    response_model=list[OrganizationWithBuilding],
    description="Поиск организации по названию",
)
async def search_organizations(
    name: str, session: AsyncSession = Depends(db_helper.session_getter)
):
    organizations = await OrganizationService.search_by_name(session=session, name=name)
    return organizations
