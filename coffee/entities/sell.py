from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask import request, current_app

from . import Base
from .shift import Shift
from .sell_coffee import SellCoffee


class Sell(Base):
    __tablename__ = 'sells'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cashier_id = Column(Integer, ForeignKey('users.id'))
    shift_id = Column(Integer, ForeignKey('shifts.id'))

    cashier = relationship('User', backref='sells')
    shift = relationship('Shift', backref='sells')

    def __init__(self, cashier, shift):
        self.cashier = cashier
        self.shift = shift

    @staticmethod
    def sell(cashier):
        db = current_app.db()

        shift = Shift.current_shift()
        if shift is None:
            return False

        new_sell = Sell(cashier, shift)
        db.add(new_sell)
        db.commit()

        sell_size = int(request.values.get('size'))
        for i in range(1, sell_size + 1):
            coffee_name = request.values.get(f'type{i}')
            number = request.values.get(f'number{i}')

            sell_coffee = SellCoffee(new_sell, coffee_name, number)
            db.add(sell_coffee)

        db.commit()

    @staticmethod
    def search():
        db = current_app.db()

        cashier_name = request.values.get('cashier')
        shift_name = request.values.get('shift')
        coffee_name = request.values.get('coffee')

        if cashier_name is None:
            return None

        match = db.query(Sell)

        if cashier_name:
            match = match.filter(Sell.cashier.has(name=cashier_name))
        if shift_name:
            match = match.filter(Sell.shift.has(name=shift_name))
        if coffee_name:
            match = match.join(SellCoffee).filter(SellCoffee.coffee_name == coffee_name)

        results = []

        for matched_sell in match:
            sell_dict = {'cashier': matched_sell.cashier.name, 'shift': matched_sell.shift.name, 'order': []}
            for record in matched_sell.sell_coffee_records:
                sell_dict['order'].append({'name': record.coffee_name, 'count': record.coffee_count})
            results.append(sell_dict)

        return results
