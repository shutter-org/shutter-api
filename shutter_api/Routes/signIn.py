from flask import request
from flask_jwt_extended import create_access_token

from shutter_api.Keys import ENCRYPTION_KEY
from shutter_api.MySQL_command import *
from shutter_api.Responses import *
from shutter_api.Tools import decrypt


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
            password = decrypt(password, ENCRYPTION_KEY)
        except:
            return missingParameterInJson("password")

        if isUserPasswordValid(username, password):
            token = create_access_token(username)
            user = getUserByUsernameLess(username)
            return connectionSucces(token, user)
        else:
            return connectionFail()
