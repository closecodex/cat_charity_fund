from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int | None = None
    create_date: datetime | None = None

    class Config:
        orm_mode = True
