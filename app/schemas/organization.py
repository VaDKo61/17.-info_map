from pydantic import BaseModel, ConfigDict, Field

from .activity import ActivityRead
from .building import BuildingRead


class OrganizationPhoneBase(BaseModel):
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str
    phones: list[OrganizationPhoneBase]
    activities: list["ActivityRead"]

    model_config = ConfigDict(from_attributes=True)


class OrganizationRead(OrganizationBase):
    id: int


class OrganizationPaginatedResponse(BaseModel):
    items: list[OrganizationRead]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=0)
    page_size: int = Field(..., ge=0)
    page_count: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)


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
