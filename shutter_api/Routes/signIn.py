from flask import request
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def signIn(app) -> None:
    
    @app.route("/signin", methods=["POST"])
    def get_signin():
        data = request.get_json()
        try:
            username = data["username"]
            if type(username) is not str:
                return connectionFail()
            username = username.strip()
            if not doesUsernameExist(username):
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
        
        

        data = {
            "username": username,
            "password": password
        }
        
        if isUserPasswordValid(data):
            return connectionSucces()
        else:
            return connectionFail()