from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChangeOfGroupsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    group_number_before: int
    group_number_after: int
    date: datetime