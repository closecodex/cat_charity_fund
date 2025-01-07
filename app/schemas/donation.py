from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationUpdate(BaseModel):
    full_amount: Optional[PositiveInt] = None
    comment: Optional[str] = None


class DonationDB(DonationBase):
    id: int
    user_id: int
    full_amount: int
    create_date: datetime
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime] = None
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class DonationResponse(BaseModel):
    id: int
    comment: Optional[str] = None
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True
