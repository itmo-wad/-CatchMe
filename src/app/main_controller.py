import logging
import os

from faker import Faker
from flask import Blueprint, send_from_directory, render_template, request
import app.services as services

from . import auth

from app import db
from app.models import Tokens, SiteAdmins

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/', methods=['GET'])
def index():
    # services.add_site_admin(username=fake.name(), email='vasya@mail.ru', passwdhash=fake.name())
    # services.set_token(token_value=fake.name(), status=True, site_admin_email='vasya@mail.ru')
    # services.add_comment(username=fake.name(), site_admin_email='vasya@mail.ru', comment_object_id=1010101, comment_text='Hello everyone')
    # logger.info(str(services.get_comment_by_comments_object_id(site_admin_email='vasya@mail.ru', comment_object_id=1010101)))
    #
    return render_template('index.html')


@main.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@main.route('/logout')
def logout():
    return auth.logout()

@main.route('/signin', methods=['POST'])
def signin():
    return auth.login(request)

@main.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# @main.route('/', methods=['POST'])
# def okey():
#     return

@main.route('/admin', methods=['GET'])
@auth.login_required
def admin():
    return render_template('admin.html')

@main.route('/list_comment', methods=['GET'])
@auth.login_required
def list_comment():
    return render_template('list_comment.html')

@main.route('/generate_key', methods=['GET'])
@auth.login_required
def generate_key():
    return render_template('generate_key.html')

@main.route('/gen_token', methods=['GET'])
@auth.login_required
def gen_token():
    token = auth.get_token()
    return token

@main.route('/js/<string:script>')
def rout_js(script):
    return send_from_directory(os.path.join(main.root_path, 'static', 'js'),
                               script)

@main.route('/css/<string:style>')
def rout_css(style):
    return send_from_directory(os.path.join(main.root_path, 'static', 'css'),
                               style)

@main.route('/img/<string:img>')
def rout_img(img):
    return send_from_directory(os.path.join(main.root_path, 'static', 'img'),
                               img)
