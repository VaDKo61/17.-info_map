from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import OrganizationRepository


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
                detail=f'Здание {building_id} не найдено'
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
                detail=f'Организации {activity_id} не найдены'
            )

        return organizations

    @staticmethod
    async def get_organizations(
            session: AsyncSession
    ):
        organizations = await OrganizationRepository.get_organization(
            session,
        )

        if not organizations:
            raise HTTPException(
                status_code=404,
                detail=f'Организации не найдены'
            )

        return organizations
