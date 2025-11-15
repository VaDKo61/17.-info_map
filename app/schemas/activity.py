from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
