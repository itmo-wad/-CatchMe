import logging
import os

from faker import Faker
from flask import  request, Blueprint, send_from_directory, render_template
from . import services

from app.models import Visitor, Comment
from . import db

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/', methods=['GET'])
def index():
    # services.add_visitor(fake.name(), 'Visitor')
    # visitor = services.get_visitor_by_username('Visitor')
    # services.add_comment(visitor, 'comment text first')
    # services.add_comment(visitor, 'second comment')

    # search = services.get_visitor_by_username('Visitor')
    # return str(Comment.query.with_parent(search).all())
    return render_template('index.html')


@main.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@main.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@main.route('/generate_key', methods=['GET'])
def generate_key():
    return render_template('generate_key.html')

@main.route('/gen_token', methods=['GET'])
# @login_required
def gen_token():
    token = services.get_token()
    return token

@main.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@main.route('/', methods=['POST'])
def okey():
    return


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
