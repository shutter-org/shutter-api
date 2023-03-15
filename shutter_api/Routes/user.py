from shutter_api.MySQL_command import *
from flask import jsonify, request
from shutter_api.Responses import *

class UserError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def user(app) -> None:
    
    @app.route("/users/<username>", methods=["GET"])
    def get_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        data = getUserByUsernname(username)
        follow = getFollowUser(username)
        followed = getFollowedUser(username)
        gallerys = getUserGallery(username)
        
        if data is None or follow is None or followed is None or gallery is None:
            return requestFail()
        
        data["following"] = follow
        data["followers"] = followed
        data["gallerys"] = gallerys
        return ok(data=data)
    
    @app.route("/users/<username>", methods=["DELETE"])
    def deleteUser(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if deleteUserFromDB(username):
            return deleteSucces()
        else:
            return deleteFail()
        
    @app.route("/users/<username>/follow", methods=["POST"])
    def post_users_username_follow(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        data = request.get_json()
        
        try:
            follow_username = data["follow_username"]
            if type(follow_username) is not str:
                return invalidParameter("follow_username")
            follow_username = follow_username.strip()
            if not doesUsernameExist(follow_username):
                return invalidParameter("follow_username")
            
        except KeyError:
            missingParameterInJson("follow_username")
        
        if username == follow_username:
            return invalidParameter("follow_username same as username")
        
        data = {
            "follower_username" : username,
            "followed_username": follow_username
        }
        if usernameFollowUser(data):
            return ok()
        else:
            return requestFail()
    
    @app.route("/users/<username>/followed/publications", methods=["GET"])
    def get_usersusername_followed_publications(username:str):
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        try:
            page = int(request.args.get('page'))
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            page = 1
        except TypeError:
            return invalidParameter("page")

        data = getuserFollowedPublication(username, offset=page)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)