from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)

    create_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Отладочный метод для представления модели."""
        return (
            f"<CharityProject(name='{self.name}', "
            f"description='{self.description}', "
            f"create_date='{self.create_date}')>"
        )
