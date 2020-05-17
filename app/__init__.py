import logging
import os
from logging.handlers import RotatingFileHandler

# from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('info.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def register_blueprints(app):
    from .main_controller import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return None


def create_db(app):
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='simple_user', pw='simple_user', url='localhost:5432',
                                                                   db='commentcloud')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(16)
    create_db(app)
    # login = LoginManager(app)
    register_blueprints(app)
    configure_logging()
    with app.app_context():
        db.create_all()
    return app
