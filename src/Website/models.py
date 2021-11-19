from sqlalchemy.orm import defaultload
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort

"""There is an ugly mistake here please act stupid"""

class Colors(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    color = db.Column(db.String(255), nullable=False)
    available_size = db.Column(db.String(255), nullable=False, default="S M L XL XXL XXXL XXXXL XXXXXL XXXXXXL")


class design(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    collection = db.Column(db.String(255), nullable=False)
    Type = db.Column(db.String(255), nullable=False)
    sold = db.Column(db.Integer, nullable=False, default=0)




class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, nullable=False, default=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_first_name = db.Column(db.String(255))
    client_last_name = db.Column(db.String(255))
    client_phone_number = db.Column(db.String(255), unique=True)
    client_city = db.Column(db.String(255))
    client_distruct = db.Column(db.String(255))
    added_by = db.Column(db.String(255))
    buying_times = db.Column(db.Integer, default=0)

    since = db.Column(db.String(255), nullable=False, default=func.now())


class Orders(db.Model):
    date = db.Column(db.String(255), nullable=False, default=func.now())
    client_number = db.Column(db.String(255), nullable=False, default='')
    author = db.Column(db.String(255), nullable=False, default='dar3en')
    Type = db.Column(db.String(255), nullable=False)
    adjustments = db.Column(db.String(255), nullable=False, default='')
    quantity = db.Column(db.Integer, nullable=False)
    tshirt_size = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    design_name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer,primary_key=True)
    done = db.Column(db.Boolean, default=False, nullable=False)


class MyModelView(ModelView):
    def is_accessible(self):
        try:
            user = User().query.filter_by(username=current_user.username).first()
            auth = True #current_user.is_authenticated didn't work here.
        except:
            abort(404)
        return auth
