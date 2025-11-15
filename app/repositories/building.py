from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from models import Building, Organization


class BuildingRepository:

    @staticmethod
    async def get_all_with_organizations(session: AsyncSession) -> list[Building]:
        query = (
            select(Building)
            .options(
                selectinload(Building.organizations)
                .selectinload(Organization.phones), selectinload(Building.organizations)
                .selectinload(Organization.activities)
            )
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_rectangle(
            session: AsyncSession,
            lat_min: float,
            lat_max: float,
            lng_min: float,
            lng_max: float
    ) -> list[Building]:
        query = (
            select(Building)
            .options(
                selectinload(Building.organizations)
                .selectinload(Organization.phones), selectinload(Building.organizations)
                .selectinload(Organization.activities)
            ).where(
                and_(
                    Building.latitude.between(lat_min, lat_max),
                    Building.longitude.between(lng_min, lng_max)
                )
            )
        )
        result = await session.execute(query)
        return list(result.scalars().all())
