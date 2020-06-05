import json
import logging
import os
import re
import socket

from faker import Faker
from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import requests as request_other

from . import auth
from .. import services

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.route('/test.add', methods=['GET'])
def add_comment_get():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    logger.info(str(IPAddr))
    data = {"username": "Lexi", "comment_object_id": "ede", "comment_text": "wefwe", "token": "ewfwe"}
    data_json = json.dumps(data)
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = request_other.post("http://172.20.0.4/add.comment", json=data_json, headers=newHeaders)
    logger.info(str(r))

    return "Okey"


@api.route('/add.comment', methods=['POST'])
def add_comment():
    logger.info(str(request.content_type))
    logger.info(str(request))
    if request.is_json:
        json_str = request.get_json()
        json_dict = json.loads(json_str)
        logger.info(str(json_dict))
        logger.info(str(type(json_dict)))
        if (("username" and "comment_object_id" and "comment_text" and "token") in json_dict) and len(json_dict) == 4:
            if check_username(json_dict['username']) and check_comment_object_id(json_dict['comment_object_id']) and \
            check_comment_text(json_dict['comment_text']) and check_token(json_dict['token']):
                username = str(json_dict['username'])
                comment_object_id = str(json_dict['comment_object_id'])
                comment_text = str(json_dict['comment_text'])
                token = str(json_dict['token'])
                site_admin_id = services.get_site_admin_id_by_token_value(token)
                if site_admin_id is not None:
                    services.add_comment(username=username, comment_object_id=comment_object_id,
                                         comment_text=comment_text, site_admin_id=site_admin_id)
                    logger.info("ADDED")
                logger.info('func --add_comment: {u, id, text} - ' + username + ", " + comment_object_id + ", " + comment_text)
                logger.info('func --add_comment: {ip-address} - ' + str(request.remote_addr))
                logger.info(str(current_user))
            return "okey"
        else:
            return "Not okey"
    return "Redirected"


def check_username(username):
    username = str(username)
    pattern = '^\w{1,16}$'
    if re.fullmatch(pattern, username) is not None:
        return username
    else:
        return None


def check_comment_object_id(comment_object_id):
    comment_object_id = str(comment_object_id)
    pattern = '^\w{1,32}$'
    if re.fullmatch(pattern, comment_object_id) is not None:
        return comment_object_id
    else:
        return None


def check_comment_text(comment_text):
    comment_text = str(comment_text)
    pattern = '^\w{1,64}$'
    if re.fullmatch(pattern, comment_text) is not None:
        return comment_text
    else:
        return None


# TODO: change the check of the size of the token and its characters
def check_token(token):
    token = str(token)
    pattern = '^\w{1,64}$'
    if re.fullmatch(pattern, token) is not None:
        return token
    else:
        return None
