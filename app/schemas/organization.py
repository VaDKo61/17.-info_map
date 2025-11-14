from pydantic import BaseModel

from models import Activity, OrganizationPhone


class OrganizationBase(BaseModel):
    name: str
    phones: list[OrganizationPhone]
    activities: list[Activity]


class OrganizationRead(OrganizationBase):
    id: int
