from pydantic import BaseModel, ConfigDict

from .building import BuildingRead
from .activity import ActivityRead


class OrganizationPhoneBase(BaseModel):
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str
    phones: list[OrganizationPhoneBase]
    activities: list['ActivityRead']

    model_config = ConfigDict(from_attributes=True)


class OrganizationRead(OrganizationBase):
    id: int


class OrganizationWithBuilding(OrganizationRead):
    building: BuildingRead


class BuildingOrganizationsResponse(BaseModel):
    building_id: int
    organizations: list[OrganizationRead]

    model_config = ConfigDict(from_attributes=True)


class ActivityOrganizationsResponse(BaseModel):
    activity_id: int
    organizations: list[OrganizationRead]

    model_config = ConfigDict(from_attributes=True)


class BuildingsAndOrganizationsResponse(BaseModel):
    buildings: list[BuildingRead]
    organizations: list[OrganizationWithBuilding]

    model_config = ConfigDict(from_attributes=True)
