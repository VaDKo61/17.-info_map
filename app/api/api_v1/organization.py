from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from models import Building, Organization

router = APIRouter(tags=['organizations'])


@router.get('/by-building/{building_id}')
async def get_organizations_by_building(
        building_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    building = await session.scalar(
        select(Building).where(Building.id == building_id)
    )
    if not building:
        raise HTTPException(status_code=404, detail='Здание не найдено')

    result = await session.execute(
        select(Organization).where(Organization.building_id == building_id)
    )
    organizations = result.scalars().all()

    return {
        'building_id': building_id,
        'organizations': [
            {
                'id': org.id,
                'name': org.name,
                'description': org.description,
            }
            for org in organizations
        ]
    }
