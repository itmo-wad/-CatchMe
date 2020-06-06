import json
import logging
import re

import requests as request_other
from flask import Blueprint, request, jsonify, make_response, Response
from flask_login import current_user

from .. import services

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.route('/test.add', methods=['GET'])
def add_comment_get():
    token = services.get_token_by_admin_email(current_user.id)
    token = token.TokenValue
    logger.info(token)
    logger.info(current_user.id)
    data = {"username": "Maxi", "comment_object_id": "grobb", "comment_text": "This is the this is"}
    data_json = json.dumps(data)
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = request_other.post("http://192.168.0.108/add.comment?token={token}".format(token=token), json=data_json, headers=newHeaders)
    return "Okey"


def validCommentObject(CommentObject):
	if CommentObject and ("username" and "comment_object_id" and "comment_text") in CommentObject:
		return True
	else:
		return False


@api.route('/add.comment', methods=['POST'])
def add_comment():
    logger.info(str(request.content_type) + ",  " + str(request))
    json_str = request.get_json()
    invalidCommentObjectErrorMsg = {
    	"error": "Invalid Comment object passed in request",
    	"helpString": "Data passed in similar to this \
        {'username': 'Ivan', 'comment_text': 'I <3 Comment Cloud', 'comment_object_id': 'something_nice' }"
    }
    response = Response(json.dumps(invalidCommentObjectErrorMsg), status=409, mimetype='application/json')
    if(validCommentObject(json_str)):
        logger.info(str(request.args.get('token')))
        logger.info(str(type(json_str)) + "  " + str(json_str))
        username = str(json_str['username'])
        comment_object_id = str(json_str['comment_object_id'])
        comment_text = str(json_str['comment_text'])
        logger.info('func --add_comment: {u, id, text} - ' + username + ", " + comment_object_id + ", " + comment_text)
        try:
            token = request.args.get('token')
            return push_comment(token, username, comment_object_id, comment_text)
        except Exception as ex:
            return make_response(str(ex), 202)
    else:
        return response


@api.route('/show', methods=['GET'])
def show_comments():
    token_value = request.args.get('token')
    logger.info(str(token_value))
    site_admin_id = services.get_site_admin_id_by_token_value(token_value)
    logger.info(str(site_admin_id))
    if site_admin_id:
        comments = services.get_comment_by_site_admin_id(site_admin_id)
        comment_database = []
        for comment in comments:
            new_comment = {
                "site_admin_id": comment.SiteAdminId,
                "username": comment.Username,
                "CommentObjectId": comment.CommentObjectId,
                "CommentText": comment.CommentText
            }
            comment_database.insert(0, new_comment)
        logger.info(str(new_comment))
    return make_response(jsonify(comment_database), 201)


def push_comment(token, username, comment_object_id, comment_text):
    site_admin_id = services.get_site_admin_id_by_token_value(token)
    logger.info(site_admin_id)
    if site_admin_id is not None:
        services.add_comment(username=username, comment_object_id=comment_object_id,
                             comment_text=comment_text, site_admin_id=site_admin_id)
        return make_response("Comment Inserted", 201)
    return make_response("Token Not valid", 401)


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


# def check_token(token):
#     token = str(token)
#     pattern = "^\w{1,256}$"
#     if re.fullmatch(pattern, token) is not None:
#         return token
#     else:
#         return None
