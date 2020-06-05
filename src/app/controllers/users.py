import flask_login
from flask import flash, redirect, url_for
from flask_login import UserMixin

from .. import login, services


# class User(UserMixin):
#     pass

class User(flask_login.UserMixin):
    def __init__(self, site_admin):
        self.site_admin = site_admin
        self.id = site_admin.Email

    def get_id(self):
        email = self.site_admin.Email
        return str(email)


# Mandatory function For flask-login
@login.user_loader
def user_loader(email):
    site_admin = services.get_site_admin_by_email(email)
    if site_admin is None:
        return None
    else:
        return User(site_admin)


@login.unauthorized_handler
def unauthorized_handler():
    flash("Please login before Пожалуйста!")
    return redirect(url_for('main.index'))
