from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Organization
from models import Building


class OrganizationRepository:
    @staticmethod
    async def get_by_building_id(
            session: AsyncSession,
            building_id: int
    ) -> list[Organization]:
        query = (
            select(Organization)
            .join(Building, Building.id == Organization.building_id)
            .where(Building.id == building_id)
        )

        result = await session.execute(query)
        return list(result.scalars().all())
