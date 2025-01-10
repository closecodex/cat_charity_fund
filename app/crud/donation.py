from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from .base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для модели Donation."""

    async def get_user_donations(
        self, session: AsyncSession, user_id: int
    ) -> list[Donation]:
        select_statement = (
            select(Donation)
            .where(Donation.user_id == user_id)
            .order_by(Donation.create_date)
        )
        result = await session.execute(select_statement)
        return result.scalars().all()


donation_crud = DonationCRUD(Donation)
