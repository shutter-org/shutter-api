from flask import request, jsonify
from shutter_api.MySQL_command import *

class CommentError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def comment(app) -> None:
    
    @app.route("/comments/<comment_id>/like", methods=["Post"])
    def postLikeComment(comment_id):
        
        data = request.get_json()
        try:
            rating = data["rating"]
            username = data["username"]
            if type(rating) is not bool:
                raise CommentError("like is not of boolean type")
            if username == "":
                raise CommentError("username param invalid")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except CommentError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "rating": int(rating),
            "comment_id": comment_id,
            "username":username
        }
        
        if likeComment(data):
            getAllRateComment()
            return jsonify({"status": "succes"}), 200
        else:
            return jsonify({"status": "Fail"}), 400
        
    @app.route("/comments/<comment_id>", methods=["DELETE"])
    def deleteComment(comment_id):
        
        if deleteCommentFromDB(comment_id):
            getAllComment()
            return jsonify({"deleted status": "succes"}),200
        else:
            return jsonify({"deleted status": "fail"}),400
    
        