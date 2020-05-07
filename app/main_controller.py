import logging

from faker import Faker
from flask import Blueprint

from app.models.users import User
from . import db

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/')
def index():
    admin = User(fake.name())
    db.session.add(admin)
    db.session.commit()
    logger.info(User.query.all())
    return 'Hello proger'


