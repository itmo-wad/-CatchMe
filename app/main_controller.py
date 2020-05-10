import logging

from faker import Faker
from flask import Blueprint
from . import services

from app.models import Visitor, Comment
from . import db

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


# @main.route('/')
# def index():
#     py = Visitor(token=fake.name(), username='Visitor')
#     logger.info(str(py))
#     Comment(comment_text='comment1', visitor=py)
#     db.session.add(py)
#     db.session.commit()
#     try:
#         visitor = db.session.query(Visitor).filter_by(username="Visitor").first()
#         logger.info(str(visitor))
#         # p = Comment(comment_text='second')
#         # visitor.comments.append(p)
#         Comment(comment_text='comment2', visitor=visitor)
#     except Exception as ex:
#         logger.warning(str(ex))
#
#     search = db.session.query(Visitor).filter_by(username="Visitor").first()
#     return str(Comment.query.with_parent(search).all())


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


