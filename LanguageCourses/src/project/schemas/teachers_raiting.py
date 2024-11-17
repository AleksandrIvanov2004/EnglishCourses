from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeachersRaitingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    teacher_id: int
    raiting: float
    actually_date: datetime