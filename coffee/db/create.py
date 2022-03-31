from .database import SessionLocal, engine
from coffee.entities import *
from werkzeug.security import generate_password_hash


def create(employees):
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)

    for employee in employees:
        db.add(User(employee['login'], generate_password_hash(employee['password']),
                    employee['type'], employee['name']))
    db.commit()
