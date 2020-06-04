import logging
import os

from faker import Faker
from flask import Blueprint, send_from_directory, render_template, request
from flask_login import login_required

from . import auth


api = Blueprint('api', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)


@api.route('/add.comment', methods=['POST'])
def add_comment():
    if request.json:
        json_dict = request.get_json()
        logger.info(str(json_dict))

    return "okey"
