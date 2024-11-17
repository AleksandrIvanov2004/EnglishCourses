from pydantic import BaseModel, ConfigDict


class TeacherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    age: int
    experience: int
    first_name: str
    second_name: str