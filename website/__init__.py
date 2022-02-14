from dotenv import find_dotenv, load_dotenv
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = 'database.db'



load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app