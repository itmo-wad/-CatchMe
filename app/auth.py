from flask import request, url_for, redirect, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user
from functools import wraps
from . import users as u
import jwt, datetime
from app import app


@app.route('/login/', methods=['POST'])
def login():
    userEmail = request.form.get('userEmail')
    userPass = request.form.get('userPass')
    if userEmail in u.user_database['User']:
        root = u.user_database['User'][userEmail]
        if check_password_hash(root['pswd'], userPass):
            user = u.User()
            user.id = userEmail
            login_user(user)
            return redirect(url_for('protected'))
    return redirect(url_for('index'))

# Token generator
def get_token():
    expiration_date = datetime.datetime.utcnow() + \
            datetime .timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date},\
            app.secret_key, algorithm='HS256')
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
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid Token'}), 401
    return wrapper
