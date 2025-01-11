from datetime import datetime

from app.models.base import InvestmentBaseModel


def process_investment(
    target: InvestmentBaseModel,
    sources: list[InvestmentBaseModel]
) -> list[InvestmentBaseModel]:
    """
    Распределяет инвестиции из источников (sources) в цель (target).
    """
    changed = []
    for source in sources:
        if target.fully_invested:
            break
        invest_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += invest_amount
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
        changed.append(source)
    return changed
