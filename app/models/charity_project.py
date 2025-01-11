from sqlalchemy import Column, Integer, String
from .base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):

    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    invested_amount = Column(Integer, default=0)

    def __repr__(self):
        """Отладочное представление модели CharityProject."""
        base_repr = super().__repr__()
        return (
            f'{base_repr[:-1]}, name={self.name}, '
            f'description={self.description})'
        )
