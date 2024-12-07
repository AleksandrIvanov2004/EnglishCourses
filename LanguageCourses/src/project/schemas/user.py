from pydantic import BaseModel, Field, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    age: int
    email: str = Field(pattern=r"^\S+@\S+\.\S+$", examples=["email@mail.ru"])
    password: str
    first_name: str
    second_name: str
    role: str