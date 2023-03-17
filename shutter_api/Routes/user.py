from shutter_api.MySQL_command import *
from flask import request
from shutter_api.Responses import *
from flask_jwt_extended import jwt_required, get_current_user
import re


def user(app) -> None:
    
    @app.route("/users/<username>", methods=["GET"])
    @jwt_required()
    def get_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username == get_current_user():
            data = getUserByUsernameDetail(username)
            gallerys = getUserGallery(username, True)
        else:
            data = getUserByUsername(username)
            gallerys = getUserGallery(username, False)
            
        following = getFollowUser(username)
        followers = getFollowedUser(username)
        
        
        if data is None or following is None or followers is None or gallery is None:
            return requestFail()
        
        data["following"] = following
        data["followers"] = followers
        if username != get_current_user():
            data["followed_by_user"] = get_current_user() in followers
            
        data["gallerys"] = gallerys
        return ok(data=data)
    
    
    @app.route("/users/<username>", methods=["PUT"])
    @jwt_required()
    def put_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
        data = request.get_json()
        try:
            newUsername = data["username"]
            if type(newUsername) is not str:
                return invalidParameter("newUsername")
            newUsername = newUsername.strip()
            if doesUsernameExist(newUsername):
                return invalidParameter("newUsername already taken")
        except KeyError:
            newUsername = None
            
        try:
            email = data["email"]
            if type(email) is not str:
                return invalidParameter("email")
            email = email.strip()
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                return invalidParameter("email")
            if not isEmailValid(email):
                return invalidParameter("email already taken") 
        except KeyError:
            email = None
            
        try:
            bio = data["biography"]
            if type(bio) is not str:
                return invalidParameter("biography")
            bio = bio.strip()
            if bio == "":
                return invalidParameter("biography")
        except KeyError:
            bio = None
            
        try:
            profile_picture = data["profile_picture"]
            if type(profile_picture) is not str:
                return invalidParameter("profile_picture")
            profile_picture = profile_picture.strip()
            if profile_picture == "":
                return invalidParameter("profile_picture")
        except KeyError:
            profile_picture = None
        
        if (profile_picture is None and bio is None and
            email is None and newUsername is None):
            return missingParameterInJson("No param")
        
        if updateUser(username, newUsername=newUsername, email=email, bio=bio, picture=profile_picture):
            return ok()
        else:
            return requestFail()
        

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
        
        
        follower = get_current_user()
            
        if username == follower:
            return invalidParameter("user cannot follow him self")
        
        if usernameFollowUser(follower=follower, followed=username):
            return ok()
        else:
            return requestFail()
        
    @app.route("/users/<username>/follow", methods=["DELETE"])
    @jwt_required()
    def delete_users_username_follow(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        follower = get_current_user()
        
        if not doesUserFollowUsername(follower=follower, followed=username):
            return noAcces()
            
        if usernameUnfollowUser(follower=follower, followed=username):
           return ok() 
        else:
            return requestFail()

        
    @app.route("/users/<username>/following", methods=["GET"])
    @jwt_required()
    def get_usersusername_following(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        

        try:
            page = request.args.get('page', default=1, type=int)
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")


        data = getFollowUser(username)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
        
    @app.route("/users/<username>/followers", methods=["GET"])
    @jwt_required()
    def get_usersusername_followers(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        

        try:
            page = request.args.get('page', default=1, type=int)
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")


        data = getFollowedUser(username)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
    
    @app.route("/users/following/publications", methods=["GET"])
    @jwt_required()
    def get_users_following_publications():
        
        username = get_current_user()
        
        try:
            page = request.args.get('page', default=1, type=int)
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")


        data = getuserFollowedPublication(username, offset=page)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)