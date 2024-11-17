from pydantic import BaseModel, ConfigDict


class StreamSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stream_number: int
    course_id: int
