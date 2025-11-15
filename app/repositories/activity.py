from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Activity


class ActivityRepository:
    @staticmethod
    async def get_child_ids(
            session: AsyncSession,
            activity_id: int
    ) -> list[int]:
        result_ids = [activity_id]

        async def fetch_children(parent_id: int):
            query = (
                select(Activity.id)
                .where(Activity.parent_id == parent_id))

            rows = (await session.execute(query)).scalars().all()

            for child_id in rows:
                result_ids.append(child_id)
                await fetch_children(child_id)

        await fetch_children(activity_id)
        return result_ids

    @staticmethod
    async def get_by_name(
            session: AsyncSession,
            name: str
    ) -> Activity | None:
        query = (
            select(Activity)
            .where(func.lower(Activity.name) == name.lower())
        )
        result = await session.execute(query)
        return result.scalars().first()
