from flask import request
from shutter_api.MySQL_command import *
from shutter_api.Responses import *
from flask_jwt_extended import create_access_token


def signIn(app) -> None:
    
    @app.route("/signin", methods=["POST"])
    def get_signin():
        data = request.get_json()
        try:
            username = data["username"]
            if type(username) is not str:
                return connectionFail()
            username = username.strip()
            print(username)
            if not doesUsernameExist(username):
                print("ok")
                return connectionFail()
        except:
            return missingParameterInJson("username")
        
        try:
            password = data["password"]
            if type(password) is not str:
                return connectionFail()
            password = password.strip()
        except:
            return missingParameterInJson("password")
        
        print("ok")
        if isUserPasswordValid(username, password):
            token = create_access_token(username)
            user = getUserByUsernameLess(username)
            return connectionSucces(token, user)
        else:
            print("faill")
            return connectionFail()