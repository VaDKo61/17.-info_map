from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import OrganizationRepository, ActivityRepository


class OrganizationService:
    @staticmethod
    async def get_organizations_in_building(
            building_id: int,
            session: AsyncSession
    ):
        organizations = await OrganizationRepository.get_by_building_id(
            session,
            building_id
        )

        if not organizations:
            raise HTTPException(
                status_code=404,
                detail=f'Здание с id: {building_id} не найдено'
            )

        return organizations

    @staticmethod
    async def get_organizations_by_activity(
            activity_id: int,
            session: AsyncSession
    ):
        organizations = await OrganizationRepository.get_by_activity_id(
            session,
            activity_id
        )

        if not organizations:
            raise HTTPException(
                status_code=404,
                detail=f'Организации с деятельностью id: {activity_id} не найдены'
            )

        return organizations

    @staticmethod
    async def get_by_organization_id(
            organization_id: int,
            session: AsyncSession
    ):
        organization = await OrganizationRepository.get_by_organization_id(
            session,
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail=f'Организация с id: {organization_id} не найдена'
            )

        return organization

    @staticmethod
    async def get_by_activity_name(
            name: str,
            session: AsyncSession
    ):
        activity = await ActivityRepository.get_by_name(
            session,
            name
        )

        if not activity:
            raise HTTPException(
                status_code=404,
                detail=f'Организации с деятельностью: {name} не найдены'
            )

        activity_ids = await ActivityRepository.get_child_ids(session, activity.id)

        organizations = await OrganizationRepository.get_by_activity_id(
            session=session,
            activity_id=activity_ids
        )

        return organizations

    @staticmethod
    async def search_by_name(
            name: str,
            session: AsyncSession
    ):
        organizations = await OrganizationRepository.search_by_name(
            session=session,
            name=name
        )

        if not organizations:
            raise HTTPException(
                status_code=404,
                detail=f'Организации с именем: {name} не найдены'
            )
        return organizations
