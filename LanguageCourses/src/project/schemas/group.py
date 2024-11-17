from pydantic import BaseModel, ConfigDict


class GroupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    group_number: int
    course_id: int