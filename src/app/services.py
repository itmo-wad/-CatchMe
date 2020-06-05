import logging

from app import db
from app.models import Comments, SiteAdmins, Tokens

logger = logging.getLogger(__name__)


def get_comment_by_comments_object_id(site_admin_email, comment_object_id):
    try:
        site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
        comments = Comments.query.with_parent(site_admin).filter(Comments.CommentObjectId == comment_object_id).all()
        return comments
    except Exception as ex:
        logger.warning('func -- get_comment_by_comments_object_id: ' + str(ex))


def add_site_admin(username, email, passwdhash):
    try:
        site_admin = SiteAdmins(Username=username, Email=email, Passwdhash=passwdhash)
        db.session.add(site_admin)
        db.session.commit()
    except Exception as ex:
        logger.warning('func -- add_site_admin: ' + str(ex))


def set_token(token_value, site_admin_email, status=True):
    try:
        token_value = str(token_value)
        site_admin_email = str(site_admin_email)
        site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
        if site_admin is not None:
            token = Tokens.query.filter(Tokens.SiteAdminId == site_admin.Id).first()
            if token is None:
                    token = Tokens(TokenValue=token_value, Status=status, SiteAdminId=site_admin.Id)
                    logger.info('func -- set_token: ' + str(token_value))
                    db.session.add(token)
                    db.session.commit()
            else:
                update_token(token_value, site_admin.Id)
    except Exception as ex:
        logger.warning('func -- set_token: ' + str(ex))


def update_token(token_value, site_admin_id):
    try:
        token = Tokens.query.filter(Tokens.SiteAdminId == site_admin_id).first()
        token.TokenValue = token_value
        db.session.commit()
    except Exception as ex:
        logger.warning('func -- update_token: ' + str(ex))


def add_comment(site_admin_id, username, comment_object_id, comment_text):
    try:
        comment = Comments(Username=username, CommentObjectId=comment_object_id,
                           CommentText=comment_text, SiteAdminId=site_admin_id)
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
        logger.warning('func -- get_site_admin_by_email: ' + str(ex))


def get_site_admin_id_by_token_value(token_value):
    try:
        token = Tokens.query.filter(Tokens.TokenValue == token_value).first()
        if token:
            return token.SiteAdminId
        else:
            return None
    except Exception as ex:
        logger.warning('func -- get_site_admin_by_token_value: ' + str(ex))


def get_token_by_admin_email(site_admin_email):
    try:
        site_admin = get_site_admin_by_email(site_admin_email)
        if site_admin is not None:
            token = Tokens.query.filter(Tokens.SiteAdminId == site_admin.Id).first()
            if token:
                return token
            else:
                return None
    except Exception as ex:
        logger.warning('func -- get_token_by_admin_email: ' + str(ex))


def get_token_by_token(token_value):
    try:
        if token_value is not None:
            token = Tokens.query.filter(Tokens.TokenValue == token_value).first()
            if token:
                return token
            else:
                return None
    except Exception as ex:
        logger.warning('func -- get_token_by_token: ' + str(ex))


def get_comment_by_site_admin_id(site_admin_email, comment_object_id):
    site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
    return Comments.query.with_parent(site_admin).filter(Comments.CommentObjectId == comment_object_id).all()


def get_comments_by_site_admin_id(site_admin_email, comment_object_id):
    try:
        site_admin = SiteAdmins.query.filter(SiteAdmins.Email == site_admin_email).first()
        comments =  Comments.query.filter(Comments.SiteAdminId == site_admin).all()
        return comments
    except Exception as ex:
        logger.warning('func -- get_comments_by_site_admin_id: ' + str(ex))


# To check
def show_tokens():
    return Tokens.query.all()


# To check
def show_comments():
    return Comments.query.all()


# To check
def show_admins():
    return SiteAdmins.query.all()
