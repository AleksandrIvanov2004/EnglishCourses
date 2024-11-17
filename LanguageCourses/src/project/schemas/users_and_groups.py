from pydantic import BaseModel, ConfigDict


class UsersAndGroupsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    group_number: int
    stream_number: int