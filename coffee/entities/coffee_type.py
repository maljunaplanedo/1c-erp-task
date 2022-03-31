from sqlalchemy import Column, Integer, String
from flask import current_app

from . import Base


class CoffeeType(Base):
    __tablename__ = 'coffee_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_list():
        db = current_app.db()
        return [(type_.id, type_.name) for type_ in db.query(CoffeeType).all()]
