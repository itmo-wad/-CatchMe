import logging
import os

from flask import Blueprint, send_from_directory, render_template
from flask import make_response, request
from flask_login import login_required
from flask_login import current_user
from faker import Faker
from .. import app

from . import auth
from . import fake_api
from .. import app, services

fake = Faker()

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', user=current_user)


@main.route('/admin', methods=['GET'])
@login_required
def admin():
    logger.info("HERE:  " + str(current_user.id))
    return render_template('admin.html')


@main.route('/list_comment', methods=['GET'])
@login_required
def list_comment():
    # TODO
    # Add filter to get comments per siteadmin
    # comments = fake_api.comment_database
    comments = services.get_comments_by_site_admin_id(current_user.id)
    return render_template('list_comment.html', comments=comments)


@main.route('/generate_key', methods=['GET'])
@login_required
def generate_key():
    tokens = services.get_token_by_admin_email(current_user.id)
    return render_template('generate_key.html', tokens=tokens)


@main.route('/save_token', methods=['GET'])
@login_required
def save_token():
    token = request.args.get('token')
    services.set_token(token, current_user.id)
    # logger.info(token)
    # logger.info(str(token))
    return "True"

@main.route('/gen_token', methods=['GET'])
@login_required
def gen_token():
    token = auth.get_token()
    logger.info(token)
    return token


@main.route('/js/<string:script>')
def rout_js(script):
    return send_from_directory(os.path.join(app.root_path, 'static', 'js'),
                               script)


@main.route('/css/<string:style>')
def rout_css(style):
    return send_from_directory(os.path.join(app.root_path, 'static', 'css'),
                               style)


@main.route('/img/<string:img>')
def rout_img(img):
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               img)


# Error handling 404
@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(render_template("error/404.html"), 404)


# Error handling 405
@app.errorhandler(405)
def bad_type(error):
    """Bad Type."""
    return make_response(render_template("error/405.html"), 405)


# Error handling 400
@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(render_template("error/400.html"), 400)


# Error handling 500
@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(render_template("error/500.html"), 500)
