from pydantic import BaseModel, Field, ConfigDict
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    age: int
    email: str
    password: str
    first_name: str
    second_name: str