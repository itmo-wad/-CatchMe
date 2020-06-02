from werkzeug.security import check_password_hash
from flask_login import UserMixin, current_user, login_required
from flask_login import logout_user, login_user
from flask import redirect, url_for, jsonify
from functools import wraps
from app import secret_key
from app import login as l
import datetime, jwt

class User(UserMixin):
    pass

user_database = {
    'User':{
        'test@t.com': {
            'name': 'Test',
            'mail': 'test@t.com',
            'uname': 'Test',
            'pswd': 'pbkdf2:sha256:150000$I7M0C4bf$406d9f83bd9777baa915b2e37299a4e53255f471e8cf7a0cfb58ad8d2fb45ad9'}
    }
}

#Mandatory function For flask-login
@l.user_loader
def user_loader(email):
    if email not in user_database['User']:
        return

    user = User()
    user.id = email
    return user

#Mandatory function For flask-login
@l.request_loader
def request_loader(request):
    userEmail = request.form.get('uname')
    if userEmail not in user_database['User']:
        return

    user = User()
    user.id = userEmail

    root = user_database['User'][userEmail]
    user.is_authenticated = check_password_hash(root['pswd'], userPass)

    return user

def login(request):
    userEmail = request.form.get('uname')
    userPass = request.form.get('psw')
    if userEmail in user_database['User']:
        root = user_database['User'][userEmail]
        if check_password_hash(root['pswd'], userPass):
            user = User()
            user.id = userEmail
            login_user(user)
            return redirect(url_for('main.admin'))
    return redirect(url_for('main.index'))

@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@l.unauthorized_handler
def unauthorized_handler():
    # flash("Please login before #Пожалуйста!")
    return redirect(url_for("main.index"))

# Token generator
def get_token():
    expiration_date = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date},\
            secret_key, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, secret_key)
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid Token'}), 401
    return wrapper
