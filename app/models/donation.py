from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import InvestmentBaseModel


class Donation(InvestmentBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(String, nullable=True)

    user = relationship('User', back_populates='donations')

    def __repr__(self):
        """Отладочное представление модели Donation."""
        return (
            f'<Donation(user_id={self.user_id}, comment={self.comment}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date})>'
        )
