from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from .base import CRUDBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для модели Donation."""

    async def get_user_donations(
        self, session: AsyncSession, user_id: int
    ) -> list[Donation]:
        return (
            await session.execute(
                select(self.model)
                .where(self.model.user_id == user_id)
                .order_by(self.model.create_date)
            )
        ).scalars().all()

    async def get_open_donations(
        self, session: AsyncSession
    ) -> list[Donation]:
        query = select(Donation).where(Donation.fully_invested.is_(False))
        result = await session.execute(query)
        return result.scalars().all()


donation_crud = DonationCRUD(Donation)
