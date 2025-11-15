from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import Organization, Activity, Building


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
                selectinload(Organization.activities, Activity.children),
                selectinload(Organization.activities, Activity.parent),
                selectinload(Organization.building),
            )
            .where(Organization.building_id == building_id)
        )

        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_activity_id(
            session: AsyncSession,
            activity_id: int
    ) -> list[Organization]:
        activity = await session.get(
            Activity,
            activity_id,
            options=[selectinload(Activity.children)]
        )
        activity_ids = [activity.id] + [child.id for child in activity.children]

        query = (
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                selectinload(Organization.activities).selectinload(Activity.children),
                selectinload(Organization.activities).selectinload(Activity.parent),
                selectinload(Organization.building),
            )
            .where(Activity.id.in_(activity_ids))

        )

        result = await session.execute(query)

        return list(result.scalars().unique().all())

    @staticmethod
    async def get_by_activity_ids(
            session: AsyncSession,
            activity_ids: list[int]
    ) -> list[Organization]:
        query = (
            select(Organization)
            .join(Organization.activities)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities).selectinload(Activity.children),
                selectinload(Organization.activities).selectinload(Activity.parent),
                selectinload(Organization.building)
            )
            .where(Activity.id.in_(activity_ids))
        )

        result = await session.execute(query)
        return list(result.scalars().unique().all())

    @staticmethod
    async def get_organization(
            session: AsyncSession,
    ) -> list[Organization]:
        query = (
            select(Organization)
            .options(
                selectinload(Organization.phones),
                selectinload(Organization.activities),
                selectinload(Organization.activities, Activity.children),
                selectinload(Organization.activities, Activity.parent),
                selectinload(Organization.building),
            )
        )

        result = await session.execute(query)
        return list(result.scalars().all())
