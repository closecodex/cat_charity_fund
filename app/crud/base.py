from typing import Generic, Optional, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.user import User

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Универсальный класс для CRUD-операций."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession,
        limit: int = 100,
        skip: int = 0
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        *,
        user: Optional[User] = None,
        commit: bool = True
    ) -> ModelType:
        data = obj_in.dict()

        if user is not None:
            data['user_id'] = user.id

        if 'name' in data:
            existing_obj = (
                await session.execute(
                    select(self.model).where(self.model.name == data['name'])
                )
            ).scalars().first()
            if existing_obj:
                raise HTTPException(
                    status_code=400,
                    detail="Object with this name already exists."
                )

        db_obj = self.model(**data)
        session.add(db_obj)

        try:
            if commit:
                await session.commit()
            await session.refresh(db_obj)
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail="IntegrityError: duplicate or invalid data."
            ) from e

        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        commit: bool = True
    ) -> ModelType:

        update_data = obj_in.dict(exclude_unset=True)

        if (
            'full_amount' in update_data and
            getattr(db_obj, 'invested_amount', None) is not None
        ):
            new_full_amount = update_data['full_amount']

            if (
                new_full_amount is not None and
                new_full_amount < db_obj.invested_amount
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Новая сумма не может быть меньше инвестированной.'
                )

        if getattr(db_obj, 'fully_invested', False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Невозможно обновить проинвестированный объект.'
            )

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        try:
            if commit:
                await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate or invalid data."
            )
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        obj_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> ModelType:

        db_obj = await self.get(obj_id, session)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Object not found"
            )

        if getattr(db_obj, 'invested_amount', 0) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Object has investments, cannot delete'
            )

        try:
            await session.delete(db_obj)
            if commit:
                await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete object. IntegrityError."
            )
        return db_obj
