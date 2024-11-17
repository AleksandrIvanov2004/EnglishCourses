from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CoursesRaitingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id: int
    raiting: float
    actually_date: datetime