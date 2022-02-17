from . import db
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash



class Users(db.Model, UserMixin):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(175), nullable=False)
    last_name = db.Column(db.String(175), nullable=False)
    email = db.Column(db.String(175), unique=True, nullable=False)
    username = db.Column(db.String(175), unique=True, nullable=False)
    password = db.Column(db.String(175), nullable=False)

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password=password, method="sha256")


class Posts(db.Model):
    

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(175))
    post_content = db.Column(db.String(10000))
    post_image = db.Column(db.LargeBinary)
    post_date = db.Column(db.DateTime(timezone=True), default = func.now())
    post_author = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, post_title, post_content, post_image, post_author):
        self.post_title = post_title
        self.post_content = post_content
        self.post_image = post_image
        self.post_author = post_author



class Favorites(db.Model):


    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id