from typing import Generic, Optional, TypeVar, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        limit: Optional[int] = None,
        skip: int = 0
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip)
        if limit is not None:
            stmt = stmt.limit(limit)

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

        db_obj = self.model(**data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        commit: bool = True
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        if commit:
            await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        obj_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> ModelType:
        db_obj = await self.get(obj_id, session)
        session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_open(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:

        stmt = (
            select(self.model)
            .where(self.model.fully_invested.is_(False))
        )
        result = await session.execute(stmt)
        return result.scalars().all()
