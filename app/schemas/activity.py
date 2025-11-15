from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ActivityRead(ActivityBase):
    id: int
    parent: ActivityBase | None
    children: list['ActivityBase']

    model_config = ConfigDict(from_attributes=True)