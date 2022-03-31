from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    __tablename__ = 'users'

    CASHIER = 0
    MANAGER = 1

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    type = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, login, password, type_, name):
        self.login = login
        self.password = password
        self.type = type_
        self.name = name
