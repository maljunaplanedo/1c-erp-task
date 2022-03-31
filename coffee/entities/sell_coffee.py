from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base


class SellCoffee(Base):
    __tablename__ = 'sell_coffee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sell_id = Column(Integer, ForeignKey('sells.id'))
    coffee_type_id = Column(Integer, ForeignKey('coffee_types.id'))
    coffee_count = Column(Integer, nullable=False)

    sell = relationship('Sell', backref='sell_coffee_records')
    coffee_type = relationship('CoffeeType',  backref='sells')

    def __init__(self, sell, coffee_type, coffee_count):
        self.sell = sell
        self.coffee_type = coffee_type
        self.coffee_count = coffee_count
