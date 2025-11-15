from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

