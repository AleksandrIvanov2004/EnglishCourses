from pydantic import BaseModel, ConfigDict


class RegisterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    age: int
    email: str
    password: str
    first_name: str
    second_name: str
    role: str