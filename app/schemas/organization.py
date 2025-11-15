from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from .activity import ActivityBase


class OrganizationPhoneBase(BaseModel):
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str
    phones: list[OrganizationPhoneBase]
    activities: list['ActivityBase']

    model_config = ConfigDict(from_attributes=True)


class OrganizationRead(OrganizationBase):
    id: int


class BuildingOrganizationsResponse(BaseModel):
    building_id: int
    organizations: list[OrganizationRead]

    model_config = ConfigDict(from_attributes=True)
