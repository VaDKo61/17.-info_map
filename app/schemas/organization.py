from pydantic import BaseModel


class OrganizationPhoneBase(BaseModel):
    phone_number: str


class OrganizationBase(BaseModel):
    name: str
    phones: list[OrganizationPhoneBase]


class OrganizationRead(OrganizationBase):
    id: int


class BuildingOrganizationsResponse(BaseModel):
    building_id: int
    organizations: list[OrganizationRead]
