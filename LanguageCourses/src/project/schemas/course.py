from pydantic import BaseModel, ConfigDict


class CourseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    language: str
    level: str