from dotenv import find_dotenv, load_dotenv
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_qrcode import QRcode
import boto3



db = SQLAlchemy()

DB_NAME = 'database.db'



load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
S3_KEY = os.getenv('ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY = os.getenv('ACCESS_SECRET_KEY')

s3 = boto3.client('s3',
                    aws_access_key_id=S3_KEY,
                    aws_secret_access_key=S3_SECRET_ACCESS_KEY
                )

BUCKET_NAME = "skfseqretimages"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@localhost:5432/seqret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    QRcode(app)

    from .models import Users, Posts, Favorites

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app



def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("- database created -")