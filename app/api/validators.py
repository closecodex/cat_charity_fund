from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, CharityProjectUpdate


async def check_charity_project_name_is_available(
        name: str,
        session: AsyncSession,
) -> None:
    if not name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Имя проекта не может быть пустым',
        )
    charity_project = await charity_project_crud.get_charity_project_by_name(
        name=name, session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProjectDB:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='В проект уже задонатили',
        )
    return charity_project


def check_object_exist(
        obj,
        detail: str = 'Такого объекта не существует'
) -> None:
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


async def check_charity_project_could_update(
        old_obj: CharityProjectDB,
        new_data: CharityProjectUpdate,
        session: AsyncSession,
) -> None:
    if not (new_data.name or new_data.description or new_data.full_amount):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Необходимо ввести новые данные',
        )
    if new_data.name:
        await check_charity_project_name_is_available(
            new_data.name, session
        )
    if new_data.description == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Описание не должно быть пустым',
        )


def check_object_dont_close(
        obj,
):
    if obj.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
