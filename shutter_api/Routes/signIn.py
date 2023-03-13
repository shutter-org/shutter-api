from flask import request, jsonify
from shutter_api.MySQL_command import *

class SighInError(Exception):
    pass

def signIn(app) -> None:
    
    @app.route("/signin", methods=["POST"])
    def get_signin():
        data = request.get_json()
        try:
            userName = data["username"]
            password = data["password"]
            
            if userName == "" or password == "":
                raise SighInError()
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except SighInError:
            return jsonify({'Invalid': "userName or Password invalid"}), 400

        data = {
            "username": userName,
            "password": password
        }
        
        if isUserPasswordValid(data):
            return jsonify({"Connection status": "Succes"}), 200
        else:
            return jsonify({"Connection status": "Fail"}), 400