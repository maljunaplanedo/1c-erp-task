from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base


class SellCoffee(Base):
    __tablename__ = 'sell_coffee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sell_id = Column(Integer, ForeignKey('sells.id'))
    coffee_name = Column(String, nullable=False)
    coffee_count = Column(Integer, nullable=False)

    sell = relationship('Sell', backref='sell_coffee_records')

    def __init__(self, sell, coffee_name, coffee_count):
        self.sell = sell
        self.coffee_name = coffee_name
        self.coffee_count = coffee_count
