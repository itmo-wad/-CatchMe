import logging

from faker import Faker
from flask import Blueprint
from . import services

from app.models import Visitor, Comment
from . import db

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/')
def index():
    services.add_visitor(fake.name(), 'Visitor')
    visitor = services.get_visitor_by_username('Visitor')
    services.add_comment(visitor, 'comment text first')
    services.add_comment(visitor, 'second comment')

    search = services.get_visitor_by_username('Visitor')
    return str(Comment.query.with_parent(search).all())


@main.route('/', methods=['POST'])
def okey():
    return


