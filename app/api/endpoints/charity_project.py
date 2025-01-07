from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.services.investment import process_investment

router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
):
    new_project = await charity_project_crud.create(project_in, session)
    await process_investment(session)
    return new_project


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch('/{project_id}', response_model=CharityProjectDB)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_superuser),
):
    db_project = await session.get(CharityProject, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail='Project not found')

    forbidden_updates = {
        'invested_amount', 'create_date', 'close_date', 'fully_invested'
    }
    update_data = project_in.dict(exclude_unset=True)
    if any(field in forbidden_updates for field in update_data):
        raise HTTPException(
            status_code=422, detail='Attempt to update restricted fields'
        )

    updated_obj = await charity_project_crud.update(
        db_obj=db_project,
        obj_in=project_in,
        session=session
    )
    return updated_obj


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_superuser),
):
    deleted_project = await charity_project_crud.remove(project_id, session)
    return deleted_project
