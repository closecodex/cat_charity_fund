from datetime import datetime
from typing import Union, List

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def process_investment(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> list[Union[CharityProject, Donation]]:

    changed_objects = []
    need = target.full_amount - target.invested_amount

    for source in sources:

        if need <= 0:
            break
        available = source.full_amount - source.invested_amount

        if available <= 0:
            continue
        invest_amount = min(need, available)
        target.invested_amount += invest_amount
        source.invested_amount += invest_amount

        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.utcnow()

        if source.invested_amount >= source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.utcnow()

        if source not in changed_objects:
            changed_objects.append(source)

        need -= invest_amount

    if target not in changed_objects:
        changed_objects.append(target)

    return changed_objects
