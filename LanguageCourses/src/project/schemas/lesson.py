from pydantic import BaseModel, ConfigDict


class LessonSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    course_id: int