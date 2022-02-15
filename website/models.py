from enum import unique
from . import db 
from flask_login import UserMixin
from sqlalchemy import func


class Users(db.Model, UserMixin):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(175))
    last_name = db.Column(db.String(175))
    email = db.Column(db.String(175), unique=True)
    username = db.Column(db.String(175), unique=True)
    password = db.Column(db.String(175))


class Posts(db.Model):
    
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(175))
    post_content = db.Column(db.String(10000))
    post_image = db.Column(db.LargeBinary)
    post_date = db.Column(db.DateTime(timezone=True), default = func.now())
    post_author = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class Favorites(db.Model):

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post'))