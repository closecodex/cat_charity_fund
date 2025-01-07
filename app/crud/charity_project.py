from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
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

    async def create(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession
    ) -> CharityProject:
        existing_project = (await session.execute(
            select(CharityProject).where(CharityProject.name == obj_in.name)
        )).scalars().first()
        if existing_project:
            raise HTTPException(
                status_code=400,
                detail='Project with this name already exists'
            )

        new_project = CharityProject(**obj_in.dict())
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        return new_project

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        if (
            obj_in.full_amount is not None and
            obj_in.full_amount < db_obj.invested_amount
        ):
            raise HTTPException(
                status_code=400,
                detail=('Новая полная сумма не может быть '
                        'меньше инвестированной суммы.')
            )

        if db_obj.fully_invested:
            raise HTTPException(
                status_code=400,
                detail=(
                    'Невозможно обновить полностью проинвестированный проект.')
            )

        update_data = obj_in.dict(exclude_unset=True)
        try:
            for field, value in update_data.items():
                setattr(db_obj, field, value)

            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail='Проект с таким названием уже существует.'
            )

        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        project_id: int,
        session: AsyncSession
    ) -> CharityProject:
        db_obj = await session.get(CharityProject, project_id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail='Project not found')

        if db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=400,
                detail='Project has investments, cannot delete'
            )

        deleted_data = db_obj

        await session.delete(db_obj)
        await session.commit()
        return deleted_data


charity_project_crud = CharityProjectCRUD(CharityProject)
