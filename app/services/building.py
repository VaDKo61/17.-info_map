import math
from typing import Optional
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from repositories import BuildingRepository, OrganizationRepository


def _haversine(lat1, lng1, lat2, lng2) -> float:
    R = 6371  # радиус Земли в км
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class BuildingService:

    @staticmethod
    async def get_buildings_from_area(
            session: AsyncSession,
            lat: Optional[float] = None,
            lng: Optional[float] = None,
            radius: Optional[float] = None,
            lat_min: Optional[float] = None,
            lat_max: Optional[float] = None,
            lng_min: Optional[float] = None,
            lng_max: Optional[float] = None,
    ):

        if all(v is not None for v in [lat_min, lat_max, lng_min, lng_max]):
            buildings = await BuildingRepository.get_by_rectangle(session, lat_min, lat_max, lng_min, lng_max)
        else:
            buildings = await BuildingRepository.get_all_with_organizations(session)

        if lat is not None and lng is not None and radius is not None:
            buildings = [b for b in buildings if _haversine(lat, lng, b.latitude, b.longitude) <= radius]

        if not buildings:
            raise HTTPException(status_code=404, detail='Здания с организациями c заданными параметрами не найдены')

        building_ids = [b.id for b in buildings]
        organizations_nested = [
            await OrganizationRepository.get_by_building_id(session, building_id)
            for building_id in building_ids
        ]
        organizations = [org for sublist in organizations_nested for org in sublist]

        return buildings, organizations
