import logging

from faker import Faker
from flask import Blueprint

from app.models import Visitor, Comment
from . import db

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/')
def index():
    # py = Category(name='Python')
    # Post(title='Hello Python!', body='Python is pretty cool', category=py)
    # p = Post(title='Snakes', body='Ssssssss')
    # py.posts.append(p)
    # db.session.add(py)

    py = Visitor(username='Visitor')
    Comment(comment_text='okey', visitor=py)
    # p = Comment(comment_text='second')
    # py.comments.append(p)
    db.session.add(py)
    return str(Comment.query.with_parent(py).all())


@main.route('/', methods=['POST'])
def okey():
    # b = request.args.get('text')
    # a = Visitor(str(b))
    #
    # visitor = Visitor("username=Visitor")
    # Comment(comment_text='okey', visitors=visitor)
    # db.session.add(a)
    # db.session.add(visitor)
    # db.session.commit()
    return str(Visitor.query.all())


