import logging
import os

from faker import Faker
from flask import Blueprint, send_from_directory, render_template
from flask_login import login_required

from . import auth

fake = Faker()

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template('admin.html')


@main.route('/list_comment', methods=['GET'])
@login_required
def list_comment():
    return render_template('list_comment.html')


@main.route('/generate_key', methods=['GET'])
@login_required
def generate_key():
    return render_template('generate_key.html')


@main.route('/gen_token', methods=['GET'])
@login_required
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