from faker import Faker
import logging

from app import db
from app.models import Visitor, Comment

logger = logging.getLogger(__name__)
fake = Faker()


def add_visitor(token, username):
    visitor = Visitor(token=fake.name(), username=str(username))
    logger.info(str(visitor))
    db.session.add(visitor)
    db.session.commit()


def get_visitor_by_username(username):
    return db.session.query(Visitor).filter_by(username=username).first()


def add_comment(visitor, comment_text):
    comment = Comment(comment_text='comment1', visitor=visitor)
    db.session.add(comment)
    db.session.commit()


