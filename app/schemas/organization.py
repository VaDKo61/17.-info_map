from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str
    phones: list['OrganizationPhone']
    activities: list['Activity']
