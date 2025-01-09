from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import InvestmentBaseModel


class Donation(InvestmentBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(String, nullable=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='donations')

    def __repr__(self):
        """Отладочное представление модели Donation."""
        return (
            f"<Donation(id={self.id}, user_id={self.user_id}, "
            f"full_amount={self.full_amount},"
            "invested_amount={self.invested_amount}, "
            f"fully_invested={self.fully_invested},"
            "create_date={self.create_date}, "
            f"close_date={self.close_date})>"
        )
