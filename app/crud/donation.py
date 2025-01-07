from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.charity_project import CharityProjectUpdate
from app.schemas.donation import DonationCreate, DonationUpdate
from .base import CRUDBase


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для модели Donation."""

    async def create(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User
    ) -> Donation:
        """Создает пожертвование от конкретного пользователя."""
        donation = Donation(
            user_id=user.id,
            full_amount=obj_in.full_amount,
            comment=obj_in.comment,
        )
        print(
            f'DEBUG: Creating donation for user {user.id} '
            f'with data {obj_in}'
        )
        session.add(donation)
        await session.commit()
        await session.refresh(donation)
        return donation

    async def get_user_donations(
        self,
        session: AsyncSession,
        user_id: int
    ) -> list[Donation]:
        """
        Возвращает все пожертвования конкретного пользователя.
        """
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.create_date)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if (
            'full_amount' in update_data and
            db_obj.full_amount < db_obj.invested_amount
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    'Нельзя установить требуемую сумму '
                    'меньше уже проинвестированной'
                ),
            )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


donation_crud = DonationCRUD(Donation)
