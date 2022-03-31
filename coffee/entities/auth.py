import string
import random

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask import request, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from . import Base
from .user import User


class Auth(Base):
    __tablename__ = 'auths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    auth_hash = Column(String, nullable=False, index=True)

    user = relationship('User', backref='auths')

    AUTH_HASH_LEN = 30
    AUTH_HASH_COOKIE_LIFESPAN = 60 * 60 * 24 * 365 * 10

    def __init__(self, user, auth_hash):
        self.user = user
        self.auth_hash = auth_hash

    @staticmethod
    def me():
        db = current_app.db()
        auth_id = request.cookies.get('auth_id')
        auth_hash = request.cookies.get('auth_hash')

        if not auth_id or not auth_hash:
            return None

        auth = db.query(Auth).get(auth_id)
        if auth is None:
            return None

        if not check_password_hash(auth.auth_hash, auth_hash):
            return None

        return auth.user

    @staticmethod
    def authorize():
        db = current_app.db()

        login = request.values.get('login')
        password = request.values.get('password')

        if Auth.me() is not None:
            return False, 'already_auth'

        user = db.query(User).filter(User.login == login).first()
        if user is None:
            return False, 'bad_account'

        if not check_password_hash(user.password, password):
            return False, 'bad_account'

        auth_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=Auth.AUTH_HASH_LEN))

        auth = Auth(user, generate_password_hash(auth_hash))
        db.add(auth)
        db.commit()

        return True, (auth.id, auth_hash)

    @staticmethod
    def unauthorize():
        db = current_app.db()

        auth_id = request.cookies.get('auth_id')
        auth_hash = request.cookies.get('auth_hash')

        if not auth_id or auth_hash is None:
            return False, 'not_authorized'

        auth_id = int(auth_id)
        auth = db.query(Auth).get(auth_id)
        if not check_password_hash(auth.auth_hash, auth_hash):
            return False, 'not_authorized'

        db.delete(auth)
        db.commit()

        return True, ''
