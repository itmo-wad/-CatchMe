import logging, json
from flask import Blueprint, make_response, jsonify
from flask import Response, request
from .auth import token_required

fake_api = Blueprint('fake_api', __name__)
logger = logging.getLogger(__name__)

comment_database = [
    {
        'Username': 'Tonton1',
        'CommentText': 'Hey !!^!!'
    },
    {
        'Username': 'Tonton2',
        'CommentText': 'Hedssdfy !!%!!!'
    },
    {
        'Username': 'Tonton3',
        'CommentText': 'Hey !!!!!!'
    },
    {
        'Username': 'Tonton4',
        'CommentText': 'Hey !!@@'
    },
    {
        'Username': 'Tonton5',
        'CommentText': 'Hey !!!&&!!!!!'
    },
    {
        'Username': 'Tonton6',
        'CommentText': 'Hey !!!!!!()!!!!!'
    }
]



@fake_api.route('/get_comment', methods=['GET'])
def get_comment():
    return make_response(jsonify(comment_database), 200)


# Think about sanitizing comments
def validCommentObject(CommentObject):
	if ("Username" in CommentObject and "CommentText" in CommentObject):
		return True
	else:
		return False

@fake_api.route('/send_comment', methods=['POST'])
@token_required
def send_comment():
	request_data = request.get_json()
	if(validCommentObject(request_data)):
		new_comment = {
			"Username": request_data['Username'],
			"CommentText": request_data['CommentText']
		}
		comment_database.insert(0, new_comment)
		response = Response("Comment Added", status=201, mimetype='application/json')
		return response
	else:
		invalidCommentObjectErrorMsg = {
			"error": "Invalid Comment object passed in request",
			"helpString": "Data passed in similar to this {'Username': 'Ivan', 'CommentText': 'I <3 Comment Cloud' }"
		}
		response = Response(json.dumps(invalidCommentObjectErrorMsg), status=400, mimetype='application/json')
		return response;


@fake_api.route('/test_api', methods=['POST'])
# @token_required
def test_api():
    return "OK"
