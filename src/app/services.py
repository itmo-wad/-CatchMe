import logging

from faker import Faker

from app import db
from app.models import Comments, SiteAdmins, Tokens

logger = logging.getLogger(__name__)
fake = Faker()


def get_comment_by_comments_object_id(site_admin_email, comment_object_id):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    return Comments.query.with_parent(site_admin).filter(Comments.CommentObjectId == comment_object_id).all()


def add_site_admin(username, email, passwdhash):
    site_admin = SiteAdmins(Username=username, Email=email, Passwdhash=passwdhash)
    logger.info(site_admin)
    db.session.add(site_admin)
    db.session.commit()


def set_token(token_value, status, site_admin_email):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    logger.info(site_admin)
    token = Tokens(TokenValue=token_value, Status=status, SiteAdmin=site_admin)
    logger.info(token)
    db.session.add(token)
    db.session.commit()


def add_comment(site_admin_email, username, comment_object_id, comment_text, parent_id=None):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    logger.info(site_admin)

    comment = Comments(Username=username, CommentObjectId=comment_object_id,
                       CommentText=comment_text, ParentId=parent_id, SiteAdmin=site_admin)
    logger.info(comment)
    db.session.add(comment)
    db.session.commit()


