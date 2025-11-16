from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from models import Organization, Activity


class OrganizationRepository:
    @staticmethod
    async def get_by_building_id(
            session: AsyncSession,
            building_id: int
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.building_id == building_id)
        )

        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_activity_id(
            session: AsyncSession,
            activity_id: int | list[int]
    ) -> list[Organization]:
        if isinstance(activity_id, int):
            activity = await session.get(
                Activity,
                activity_id,
                options=[selectinload(Activity.children)]
            )
            if not activity:
                return []
            activity_id = [activity.id] + [child.id for child in activity.children]

        query = (
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Activity.id.in_(activity_id))

        )

        result = await session.execute(query)

        return list(result.scalars().unique().all())

    @staticmethod
    async def get_by_organization_id(
            session: AsyncSession,
            organization_id: int
    ) -> Organization:
        query = (
            select(Organization)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                joinedload(Organization.building),
            )
            .where(Organization.id == organization_id)
        )

        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def search_by_name(
            session: AsyncSession,
            name: str
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.name.ilike(f'%{name}%'))
        )

        result = await session.execute(query)
        return list(result.scalars().unique().all())
