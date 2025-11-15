from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float
