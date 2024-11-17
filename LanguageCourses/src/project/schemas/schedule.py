from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScheduleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    group_number: int
    lesson_id: int
    start_lesson: datetime
    end_lesson: datetime