from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default ='', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email,first_name = '', last_name='', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(200), nullable = True)
    sale_price = db.Column(db.Integer)
    color = db.Column(db.String(150))
    year = db.Column(db.Integer)
    new_used = db.Column(db.String(20))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, sale_price, color, year, new_used, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.sale_price = sale_price
        self.color = color
        self.year = year
        self.new_used = new_used
        self.user_token = user_token

    def __repr__(self):
        return f'The following Car has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

class CarSchema(ma.Schema):
    fields = ['id', 'make', 'model', 'sale_price', 'color', 'year', 'new_used']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)