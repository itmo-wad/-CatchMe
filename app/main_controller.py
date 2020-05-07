import logging

from flask import Blueprint
from . import db
from .user import User

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/')
def index():
    admin = User('admin', 'user@gmail.com')
    guest = User('guest', 'guest@gmail.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    logger.info(User.query.all())
    return 'Hello proger'
