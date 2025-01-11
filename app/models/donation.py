from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import InvestmentBaseModel


class Donation(InvestmentBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(String, nullable=True)

    user = relationship('User', back_populates='donations')

    def __repr__(self):
        """Отладочное представление модели Donation."""
        base_repr = super().__repr__()
        return (
            f'{base_repr[:-1]}, user_id={self.user_id}, '
            f'comment={self.comment})'
        )
