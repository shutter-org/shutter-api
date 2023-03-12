from flask import jsonify, request
from datetime import datetime
from shutter_api.MySQL_command import *
import re

class SighUnError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def signUp(app) -> None:
    
    @app.route("/signup", methods=["POST"])
    def post_signUp():
        
        data = request.get_json()
        try:
            userName = data["username"].strip()
            password = data["password"].strip()
            email = data["email"].strip()
            name = data["name"].strip()
            try:
                birthdate = datetime.strptime(data["birthdate"].strip(), '%Y/%m/%d')
            except ValueError:
                raise SighUnError("invalid birthdate")
            bio = data["bio"].strip()
            
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    

            if userName == "":
                raise SighUnError("invalid username")
            if doesUsernameExist(userName):
                raise SighUnError("username already taken")
            if password == "":
                raise SighUnError("invalid password")
            if not re.match(pattern, email):
                raise SighUnError("invalid email")
            if not isEmailValid(email):
                raise SighUnError("email already taken")
            if name == "":
                raise SighUnError("invalid name")
            
            if birthdate.date() > datetime.now().date():
                raise SighUnError("invalid birthdate")
            
            if bio == "":
                raise SighUnError("invalid bio")
            
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except SighUnError as e:
            return jsonify({'Invalid': e.args[0]}), 400
        
        
        
        data = {
            "username": userName,
            "password": password,
            "email": email,
            "name": name,
            "birthdate": birthdate,
            "biography": bio,
            "created_date" : datetime.utcnow().replace(microsecond=0).isoformat()
        }
        
        if createNewUser(data):
            getAllUser()
            return jsonify({"username" : userName}),201
        else:
            return jsonify({"Creation status" : "fail"}),400
        
        
        