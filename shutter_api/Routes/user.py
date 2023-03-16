from shutter_api.MySQL_command import *
from flask import request
from shutter_api.Responses import *
from flask_jwt_extended import jwt_required, get_current_user


def user(app) -> None:
    
    @app.route("/users/<username>", methods=["GET"])
    @jwt_required()
    def get_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        data = getUserByUsernname(username)
        following = getFollowUser(username)
        followers = getFollowedUser(username)
        gallerys = getUserGallery(username)
        
        if data is None or following is None or followers is None or gallery is None:
            return requestFail()
        
        data["following"] = following
        data["followers"] = followers
        data["followed_by_user"] = get_current_user() in followers
        data["gallerys"] = gallerys
        return ok(data=data)
    
    @app.route("/users/<username>/details", methods=["GET"])
    @jwt_required()
    def get_users_username_details(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
        data = getUserByUsernnameDetail(username)
        following = getFollowUser(username)
        followers = getFollowedUser(username)
        gallerys = getUserGallery(username)
        
        if data is None or following is None or followers is None or gallery is None:
            return requestFail()
        
        data["following"] = following
        data["followers"] = followers
        data["gallerys"] = gallerys
        return ok(data=data)
    
    #TODO
    @app.route("/users/<username>", methods=["PUT"])
    @jwt_required()
    def put_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
        data = request.get_json()
        
    
    
    @app.route("/users/<username>", methods=["DELETE"])
    @jwt_required()
    def deleteUser(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
        if deleteUserFromDB(username):
            return deleteSucces()
        else:
            return deleteFail()
        
        
    @app.route("/users/<username>/follow", methods=["POST"])
    @jwt_required()
    def post_users_username_follow(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
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
    @jwt_required()
    def get_usersusername_followed_publications(username:str):
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
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