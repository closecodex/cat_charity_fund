from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from .base import CRUDBase


class CharityProjectCRUD(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """CRUD-операции для CharityProject."""

    async def get_charity_project_by_name(
        self, name: str, session: AsyncSession
    ) -> Optional[CharityProject]:
        result = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
