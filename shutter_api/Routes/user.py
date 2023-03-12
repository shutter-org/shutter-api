from shutter_api.MySQL_command import *
from flask import jsonify, request

class UserError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def user(app) -> None:
    
    @app.route("/users/<username>", methods=["GET"])
    def get_users_username(username):
        data = getUserByUsernname(username)
        print(data)
        follow = getFollowUser(username)
        print(follow)
        followed = getFollowedUser(username)
        print(followed)
        
        if data is None or follow is None or followed is None:
            return jsonify({"Error": "username does not exist"}),400
        
        data["follow"] = follow
        data["followed"] = followed
        return jsonify(data),200
    
    @app.route("/users/<username>", methods=["DELETE"])
    def deleteUser(username):
        if deleteUserFromDB(username):
            return jsonify({"deleted status": "succes"}),200
        else:
            return jsonify({"deleted status": "fail"}),400
        
    @app.route("/users/<username>/follow", methods=["POST"])
    def post_users_username_follow(username):
        data = request.get_json()
        try:
            follow_username = data["follow_username"]
            
            if username == follow_username:
                raise UserError("username and follow_username are the same")
            if username == "" or not doesUsernameExist(username):
                raise UserError("username param invalid")
            if follow_username == "" or not doesUsernameExist(follow_username):
                raise UserError("follow_username param invalid")
            
            
            
                
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except UserError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "follower_username" : username,
            "followed_username": follow_username
        }
        getALLFollow()
        if usernameFollowUser(data):
            return "ok", 201
        else:
            return jsonify({"creation status": "Fail"}), 400
    
    @app.route("/users/<username>/followed/publications", methods=["GET"])
    def get_usersusername_followed_publications(username):
        
        if username == "" or not doesUsernameExist(username):
            return jsonify({'error': "username param invalid"}), 400
        
        data = getuserFollowedPublication(username)
        if data is None:
            return jsonify({'error': "username invalid"}), 400
        else:
            return jsonify({"Followed_publication": data}),200