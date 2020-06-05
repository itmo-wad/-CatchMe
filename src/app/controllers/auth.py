import datetime
import logging
from functools import wraps

import jwt
from flask import make_response
from flask import request, url_for, redirect, jsonify, Blueprint, render_template
from flask_login import current_user, login_required
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .users import User
from .. import app, services

auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth.route('/login', methods=['GET'])
def login():
    try:
        current_user.id
        return redirect(url_for("main.admin"))
    except:
        return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route('/register', methods=['GET'])
def register():
    try:
        current_user.id
        return redirect(url_for("main.admin"))
    except:
        return render_template('register.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('username')
    password = request.form.get('password')
    logger.info(str(email) + "  " + str(password))
    site_admin = services.get_site_admin_by_email(email)
    if site_admin:
        logger.warning(str(check_password_hash(site_admin.Passwdhash, password)))
        logging.warning(str(site_admin.Passwdhash))
        logging.warning(str(site_admin))
        if check_password_hash(site_admin.Passwdhash, password):
            login_user(User(site_admin))
            logger.info(str(current_user))
            return redirect(url_for('main.admin'))
    return "ERROR"


@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    site_admin = services.get_site_admin_by_email(email)
    if site_admin:
        return redirect(url_for('auth.register'))
    try:
        services.add_site_admin(username, email, generate_password_hash(password, method='sha256'))
    except Exception as ex:
        logger.warning(ex)
    return redirect(url_for('auth.login'))


# Token generator
def get_token():
    expiration_date = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=36000)
    token = jwt.encode({'exp': expiration_date}, app.secret_key, algorithm='HS256')
    services.set_token(token, current_user.id)
    logger.info(str(services.get_site_admin_id_by_token_value(token)))
    logger.info(str(services.show()))
    return token


# Token decorator
# When called you need to pass a valid
# token under the variable token
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.secret_key)
            logger.info(str(token))
            token = services.get_token_by_token(token)
            logger.info(str(token.Status))
            if token.Status == True:
                return f(*args, **kwargs)
        except:
            return make_response(jsonify({'error': 'Need a valid Token'}), 401)
    return wrapper
