from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login

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
@login.user_loader
def user_loader(email):
    if email not in user_database['User']:
        return

    user = User()
    user.id = email
    return user

#Mandatory function For flask-login
@login.request_loader
def request_loader(request):
    userEmail = request.form.get('userEmail')
    if userEmail not in user_database['User']:
        return

    user = u.User()
    user.id = userEmail

    root = user_database['User'][userEmail]
    user.is_authenticated = check_password_hash(root['pswd'], userPass)

    return user
