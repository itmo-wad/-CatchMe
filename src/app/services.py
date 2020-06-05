import logging

from app import db
from app.models import Comments, SiteAdmins, Tokens

logger = logging.getLogger(__name__)


def get_comment_by_comments_object_id(site_admin_email, comment_object_id):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    return Comments.query.with_parent(site_admin).filter(Comments.CommentObjectId == comment_object_id).all()


def add_site_admin(username, email, passwdhash):
    try:
        site_admin = SiteAdmins(Username=username, Email=email, Passwdhash=passwdhash)
        db.session.add(site_admin)
        db.session.commit()
    except Exception as ex:
        logger.warning('func -- add_site_admin: ' + str(ex))


def set_token(token_value, status, site_admin_id):
    try:
        site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
        token = Tokens(TokenValue=token_value, Status=status, SiteAdmin=site_admin)
        logger.info(token)
        db.session.add(token)
        db.session.commit()
    except Exception as ex:
        logger.warning('func -- set_token: ' + str(ex))


def add_comment(site_admin_id, username, comment_object_id, comment_text, parent_id=None):
    try:
        comment = Comments(Username=username, CommentObjectId=comment_object_id,
                           CommentText=comment_text, ParentId=parent_id, SiteAdmin=site_admin_id)
        logger.info(comment)
        db.session.add(comment)
        db.session.commit()
    except Exception as ex:
        logger.warning('func -- add_comment: ' + str(ex))


def get_site_admin_by_email(site_admin_email):
    try:
        site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
        if site_admin:
            return site_admin
        else:
            return None
    except Exception as ex:
        logger.info('func -- get_site_admin_by_email: ' + str(ex))


def get_site_admin_by_username(site_admin_username):
    try:
        site_admin = SiteAdmins.query.filter(SiteAdmins.Username == site_admin_username).first()
        if site_admin:
            return site_admin
        else:
            return None
    except Exception as ex:
        logger.info('func -- get_site_admin_by_username: ' + str(ex))


def get_site_admin_id_by_token_value(token_value):
    try:
        token = Tokens.query.filter(Tokens.TokenValue == token_value).first()
        if token:
            return token.SiteAdminID
        else:
            return None
    except Exception as ex:
        logger.info('func -- get_site_admin_by_token_value: ' + str(ex))


def get_comment_by_site_admin_id(site_admin_email, comment_object_id):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    return Comments.query.with_parent(site_admin).filter(Comments.CommentObjectId == comment_object_id).all()

