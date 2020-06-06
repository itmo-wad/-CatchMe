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
        return render_template('login.html', error="")


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
    site_admin = services.get_site_admin_by_email(email)
    if site_admin:
        if check_password_hash(site_admin.Passwdhash, password):
            login_user(User(site_admin))
            return redirect(url_for('main.admin'))
    return "ERROR"


@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    site_admin = services.get_site_admin_by_email(email)
    if site_admin:
        return redirect(url_for('auth.login'))
    try:
        services.add_site_admin(username, email, generate_password_hash(password, method='sha256'))
        return redirect(url_for('auth.login'))
    except Exception as ex:
        logger.warning(ex)
    return redirect(url_for('auth.register'))


# Token generator
def get_token():
    expiration_date = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=36000)
    token = jwt.encode({'exp': expiration_date}, app.secret_key, algorithm='HS256')
    # token = token[2:-1]
    services.set_token(token, current_user.id)
    logger.info(token)
    return token


# Token decorator
# When called you need to pass a valid
# token under the variable token
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_value = request.args.get('token')
        try:
            logger.info('token_required:  ' + str(token_value))
            # str(jwt.decode(token_value, app.secret_key))
            token = services.get_token_by_token(token_value)
            logger.info(str(token.Status))
            if token.Status == True:
                return f(*args, **kwargs)
        except:
            return make_response(jsonify({'error': 'Need a valid Token'}), 401)
    return wrapper
