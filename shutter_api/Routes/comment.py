from flask import request
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def comment(app) -> None:
    
    @app.route("/comments/<comment_id>", methods=["GET"])
    def get_comments_commentId(comment_id):
        
        data = getCommentById(comment_id)
        
        if data is None:
            return invalidParameter("comment_id")
        else:
            return ok(data)
    
    @app.route("/comments/<comment_id>/like", methods=["Post"])
    def post_comments_commentId_like(comment_id):
        
        data = request.get_json()
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")
        
        try:
            username = data["username"]
            if type(username) is not str:
                return invalidParameter("username")
            username = username.strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except KeyError:
            return missingParameterInJson("username")

        
        
        data = {
            "rating": int(rating),
            "comment_id": comment_id,
            "username":username
        }
        
        if likeComment(data):
            return creationSucces()
        else:
            return creationFail()
        
    @app.route("/comments/<comment_id>", methods=["DELETE"])
    def delete_comments_commentID(comment_id):
        
        if deleteCommentFromDB(comment_id):
            return deleteSucces()
        else:
            return deleteFail()
    
        