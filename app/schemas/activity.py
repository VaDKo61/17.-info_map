from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    children: list['Activity']
    organization: list['Organization']
