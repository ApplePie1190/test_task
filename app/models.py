from app import db, login_manager
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    password = Column(String(500))
    is_admin =Column(Integer(), default=0)

    def check_password(self,  password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<id:{self.id} username:{self.username} password:{self.password} is_admin:{self.is_admin}>"


class Requisites(db.Model):
    __tablename__ = 'requisites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(50))
    payment_type = Column(String(50))
    account_type = Column(String(50))
    owner_name = Column(String(100))
    phone_number = Column(String(20))
    limit = Column(Float)

    def __repr__(self):
        return f"<id:{self.id} account:{self.account} payment_type:{self.payment_type} account_type:{self.account_type} owner_name:{self.owner_name} phone_number:{self.phone_number} limit:{self.limit}>"


class PaymentRequests(db.Model):
    __tablename__ = 'payment_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float)
    status = Column(String(50))
    requisites_id = Column(Integer, ForeignKey('requisites.id'))
    requisites = db.relationship('Requisites', backref='payment_requests')

    def __repr__(self):
        return f"<id:{self.id} amount:{self.amount} status:{self.status}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)







