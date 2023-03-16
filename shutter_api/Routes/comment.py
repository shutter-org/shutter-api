from flask import request
from flask_jwt_extended import jwt_required, get_current_user
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def comment(app) -> None:
    
    @app.route("/comments/<comment_id>", methods=["GET"])
    @jwt_required()
    def get_comments_commentId(comment_id:str):
        
        if not doesCommentExist(comment_id):
            return invalidParameter("comment_id")
        
        data = getCommentById(comment_id)
        
        if data is None:
            return invalidParameter("comment_id")
        else:
            return ok(data)
        
    @app.route("/comments/<comment_id>", methods=["DELETE"])
    @jwt_required()
    def delete_comments_commentID(comment_id:str):
        
        if not doesCommentExist(comment_id):
            return invalidParameter("comment_id")
        
        username = get_current_user()
        
        if not canUserDeleteComment(username, comment_id):
            return noAcces()
        
        if deleteCommentFromDB(comment_id):
            return deleteSucces()
        else:
            return deleteFail()
        
    @app.route("/comments/<comment_id>/like", methods=["Post"])
    @jwt_required()
    def post_comments_commentId_like(comment_id:str):
        
        if not doesCommentExist(comment_id):
            return invalidParameter("comment_id")
        
        data = request.get_json()
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")
        
        username = get_current_user()

        
        
        data = {
            "rating": int(rating),
            "comment_id": comment_id,
            "username":username
        }
        
        if likeComment(data):
            return creationSucces()
        else:
            return creationFail()
    
        