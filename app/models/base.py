from sqlalchemy import (
    Column, DateTime, Integer, Boolean,
    func, CheckConstraint
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
    create_date = Column(DateTime, default=func.now(), nullable=False)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_positive'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_not_exceed_full'
        ),
    )

    def __repr__(self):
        """
        Отладочный метод для представления модели.
        """
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, invested_amount={self.invested_amount}, "
            f"fully_invested={self.fully_invested},"
            "create_date={self.create_date}, "
            f"close_date={self.close_date})>"
        )
