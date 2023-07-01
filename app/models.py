from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
from time import time
from flask import current_app
import jwt

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(20),unique = True, nullable = False)

    def __repr__(self):
        return '<Location {}>'.format(self.name)
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(20),unique = True ,nullable = False)
    qty = db.Column(db.Integer, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref="category")
    
    def __repr__(self):
        return '<Product {}>'.format(self.name)
    
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique = True ,nullable = False)
 
    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
class Transfer(db.Model):
    __tablename__ = 'transfer'
    id = db.Column(db.Integer, primary_key= True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    floc_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    tloc_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    floc = db.relationship('Location', foreign_keys=[floc_id])
    tloc = db.relationship('Location', foreign_keys=[tloc_id])
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', foreign_keys=[product_id])
    qty = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<Transfer {}>'.format(self.id)
    
class Balance(db.Model):
    __tablename__ = 'balance'
    id = db.Column(db.Integer, primary_key= True,nullable = False)
    loc_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    loc = db.relationship('Location', foreign_keys=[loc_id])
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', foreign_keys=[product_id])
    qty = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<Balance {}>'.format(self.id)