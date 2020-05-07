import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .user import User


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


def create_app():
    app = Flask(__name__)
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='user1', pw='user1', url='localhost:5432', db='commentcloud')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.create_all()

    from .main_controller import main as main_blueprint
    app.register_blueprint(main_blueprint)

    logger = configure_logging()
    return app
