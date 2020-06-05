import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from . import secrets as s

db = SQLAlchemy()
secret_key = os.urandom(16)


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
    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.auth import auth
    app.register_blueprint(auth)

    from .controllers.api import api
    app.register_blueprint(api)

    from .controllers.fake_api import fake_api
    app.register_blueprint(fake_api)
    return None


def create_db(app):
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=s.user, pw=s.pw, url=s.url,
                                                                   db=s.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)


app = Flask(__name__, static_folder='./static/', template_folder='./templates/')
app.secret_key = secret_key
create_db(app)
login = LoginManager(app)
register_blueprints(app)
configure_logging()
with app.app_context():
    db.create_all()
