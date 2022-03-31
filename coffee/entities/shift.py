from sqlalchemy import Column, Integer, Boolean, String

from flask import current_app

from . import Base


class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    open = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.open = True
        self.name = name

    @staticmethod
    def open_new(name):
        db = current_app.db()
        new = Shift(name)
        db.add(new)
        db.commit()

    @staticmethod
    def current_shift():
        db = current_app.db()
        return db.query(Shift).filter(Shift.open).first()

    @staticmethod
    def close_current():
        db = current_app.db()
        current = Shift.current_shift()
        if current is None:
            return
        current.open = False
        db.commit()

    @staticmethod
    def get_list():
        db = current_app.db()
        return [(shift.id, shift.name) for shift in db.query(Shift).all()]
