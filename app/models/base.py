from datetime import datetime
from sqlalchemy import (
    Column, DateTime, Integer, Boolean, CheckConstraint
)

from app.core.db import Base


class InvestmentBaseModel(Base):
    """
    Базовая модель для объектов инвестиций.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range'
        ),
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
    )

    def __repr__(self):
        """
        Отладочный метод для представления модели.
        """
        return (
            f'<{type(self).__name__}('
            f'{self.id=}, {self.invested_amount=}, {self.fully_invested=}, '
            f'{self.create_date=}, {self.close_date=})>'
        )
