from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationResponse
)
from app.services.investment import process_investment

router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    new_donation = await donation_crud.create(donation_in, session, user=user)
    open_projects = await charity_project_crud.get_open(session)
    session.add_all(process_investment(new_donation, open_projects))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationResponse])
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    return await donation_crud.get_user_donations(session, user.id)


@router.get('/', response_model=list[DonationDB])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
):
    return await donation_crud.get_multi(session)
