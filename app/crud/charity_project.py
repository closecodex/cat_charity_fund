from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from .base import CRUDBase


class CharityProjectCRUD(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """CRUD-операции для CharityProject."""

    async def get_open_projects(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        query = (
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
        )
        result = await session.execute(query)
        return result.scalars().all()


charity_project_crud = CharityProjectCRUD(CharityProject)
