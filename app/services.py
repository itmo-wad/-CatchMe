from faker import Faker
import logging

from app import db, secret_key
from app.models import Visitor, Comment

import jwt, datetime

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

# Token generator
def get_token():
    expiration_date = datetime.datetime.utcnow() + \
            datetime .timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date},\
            secret_key, algorithm='HS256')
    return token
