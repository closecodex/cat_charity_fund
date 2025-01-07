from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def process_investment(session: AsyncSession) -> None:

    projects_query = (
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(asc(CharityProject.create_date))
    )
    projects_result = await session.execute(projects_query)
    open_projects = projects_result.scalars().all()

    donations_query = (
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(asc(Donation.create_date))
    )
    donations_result = await session.execute(donations_query)
    open_donations = donations_result.scalars().all()

    project_index = 0
    donation_index = 0

    while (
        project_index < len(open_projects) and
        donation_index < len(open_donations)
    ):
        project = open_projects[project_index]
        donation = open_donations[donation_index]
        need = project.full_amount - project.invested_amount
        available = donation.full_amount - donation.invested_amount
        invest_amount = min(need, available)
        project.invested_amount += invest_amount
        donation.invested_amount += invest_amount

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            from datetime import datetime
            project.close_date = datetime.utcnow()

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            from datetime import datetime
            donation.close_date = datetime.utcnow()

        if project.fully_invested:
            project_index += 1

        if donation.fully_invested:
            donation_index += 1
