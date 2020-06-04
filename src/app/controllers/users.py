from flask import flash, redirect, url_for
from flask_login import UserMixin

from .. import login, services


class User(UserMixin):
    pass


# Mandatory function For flask-login
@login.user_loader
def user_loader(email):
    if not services.get_site_admin_by_email(email):
        return None
    user = User()
    user.id = email
    return user


@login.unauthorized_handler
def unauthorized_handler():
    flash("Please login before Пожалуйста!")
    # return redirect(url_for("main.index"))
    return "WTF !!"
