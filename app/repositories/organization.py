from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

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
                selectinload(Organization.activities, Activity.children),
                selectinload(Organization.building),
            )
            .where(Organization.building_id == building_id)
        )

        result = await session.execute(query)
        return list(result.scalars().all())
