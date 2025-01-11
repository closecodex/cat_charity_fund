from sqlalchemy import Column, Integer, String
from .base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):

    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    invested_amount = Column(Integer, default=0)

    def __repr__(self):
        """Отладочное представление модели CharityProject."""
        return (
            f'CharityProject(name={self.name}, '
            f'description={self.description}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date})'
        )
