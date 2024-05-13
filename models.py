from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), index=True, unique=True)
    organization = Column(String(128))
    password_hash = Column(String(128))
    is_active = Column(Boolean, default=True)
    data = relationship('Data', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, organization={self.organization}, is_active={self.is_active})>"

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    market = Column(String(64))
    category = Column(String(64))
    commodity = Column(String(64))
    unit = Column(String(64))
    currency = Column(String(64))
    price = Column(Float)
    usdprice = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Data {}>'.format(self.market)
