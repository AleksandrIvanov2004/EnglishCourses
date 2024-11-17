from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaymentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    course_id: int
    pay_date: datetime