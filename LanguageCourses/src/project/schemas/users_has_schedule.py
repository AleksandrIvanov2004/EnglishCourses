from pydantic import BaseModel, ConfigDict
from typing import Optional


class UsersHasScheduleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    schedule_id: int
    attendance: bool
    mark: Optional[int]