from shutter_api.MySQL_command import *
from flask import request
from shutter_api.Responses import *
from shutter_api.Keys import ENCRYPTION_KEY
from shutter_api.Tools import decrypt
from flask_jwt_extended import jwt_required, get_current_user, create_access_token
import re


def user(app) -> None:
    
    @app.route("/users", methods=["GET"])
    @jwt_required()
    def get_users():
        try:
            search = request.args.get('search', default="", type=str)
        except ValueError:
            search = ""
        
        data = getUsers(search)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
        
    @app.route("/users/<username>", methods=["GET"])
    @jwt_required()
    def get_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        currentUser = get_current_user()
        
        if username == currentUser:
            data = getUserByUsernameDetail(username)
            galleries = getUserGallery(username, True)
        else:
            data = getUserByUsername(username)
            galleries = getUserGallery(username, False)
            
        following = getFollowUser(username)
        followers = getFollowedUser(username)
        publications = getUserPublications(username)
        nb_following = getFollowUserNumber(username)
        nb_followers = getFollowedUserNumber(username)
        nb_publications = getNumberOfPublicationFromUser(username)
        
        
        if (data is None or following is None or
            followers is None or gallery is None or 
            publications is None or nb_followers is None or
            nb_following is None or nb_publications is None):
            return requestFail()
        
        data["following"] = following
        data["nb_following"] = nb_following
        data["nb_followers"] = nb_followers
        data["nb_publications"] = nb_publications
        data["followers"] = followers
        data["publications"] = publications
        
        if username != currentUser:
            data["followed_by_user"] = doesUserFollowUsername(currentUser,username)
            
        data["galleries"] = galleries
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
            if newUsername.find("/") != -1:
                return invalidParameter("newUsername contain '/'")
            elif newUsername.find(" ") != -1:
                return invalidParameter("username contain spacebar")
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
                return invalidParameter("email format not valid")
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
                return invalidParameter("biography empty")
        except KeyError:
            bio = None
            
        try:
            profile_picture = data["profile_picture"]
            if type(profile_picture) is not str:
                return invalidParameter("profile_picture")
            if bool(re.match('^[01]*$', profile_picture)):
                return invalidParameter("profile_picture")
        except KeyError:
            profile_picture = None
            
        try:
            name = data["name"]
            if type(name) is not str:
                return invalidParameter("name")
            name = name.strip()
            if name == "":
                return invalidParameter("name empty")
        except KeyError:
            name = None
            
        try:
            password = data["password"]
            if type(password) is not str:
                return invalidParameter("password")
            password = decrypt(password,ENCRYPTION_KEY)
            if len(password) < 5:
                return invalidParameter("password too short")
        except KeyError:
            password = None
        
        if (profile_picture is None and bio is None and
            email is None and newUsername is None and
            name is None and password is None):
            return missingParameterInJson("No param")
        
        if updateUser(username, newUsername=newUsername, email=email, bio=bio, picture=profile_picture, name=name, password=password):
            if newUsername is not None:
                token = create_access_token(newUsername)
                user = getUserByUsernameLess(newUsername)
                return connectionSucces(token, user)
            
            if profile_picture is not None:
                user = getUserByUsernameLess(username)
                return ok(data=user)
            
            return ok()
        else:
            return requestFail()
        
    @app.route("/users/<username>", methods=["DELETE"])
    @jwt_required()
    def delete_users_username(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        if username != get_current_user():
            return noAcces()
        
        if deleteUserFromDB(username):
            return deleteSucces()
        else:
            return deleteFail()
      
    @app.route("/users/<username>/publications", methods=["GET"])
    @jwt_required()
    def get_users_username_publications(username:str):
        
        username = username.strip()
        if not doesUsernameExist(username):
            return invalidParameter("username")
        
        try:
            page = request.args.get('page', default=1, type=int)
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")
        data = getUserPublications(username, offset=page)
        if data is not None:
            return ok(data=data)
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

        data = {
            "publications" : getUserFollowedPublication(username, offset=page),
            "nb_publications" : getNbUserFollowedPublications(username)
        }
        
        if data["publications"] is None or data["nb_publications"] is None:
            return requestFail()
        else:
            return ok(data=data)