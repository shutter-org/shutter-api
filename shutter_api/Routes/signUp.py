from flask import request
from datetime import datetime
from shutter_api.MySQL_command import *
from shutter_api.Responses import *
import re

def signUp(app) -> None:
    
    @app.route("/signup", methods=["POST"])
    def post_signUp():
        
        data = request.get_json()
        try:
            username = data["username"]
            if type(username) is not str:
                return invalidParameter("username")
            username = username.strip()
            if username.find("/") != -1:
                return invalidParameter("username contain '/'")
            if doesUsernameExist(username):
                return invalidParameter("username")
        except KeyError:
            return missingParameterInJson("username")
        
        try:
            password = data["password"]
            if type(password) is not str:
                return invalidParameter("password")
            password = password.strip()
            if len(password) <= 5:
                return invalidParameter("password")
        except KeyError:
            return missingParameterInJson("password")
        
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
            return missingParameterInJson("email")
        
        try:
            name = data["name"]
            if type(name) is not str:
                return invalidParameter("name")
            name = name.strip()
            if name == "":
                return invalidParameter("name")
        except KeyError:
            return missingParameterInJson("name")
        
        try:
            birthdate = data["birthdate"]
            if type(birthdate) is not str:
                return invalidParameter("birthdate")
            birthdate = birthdate.strip()
            birthdate = datetime.strptime(birthdate, '%Y/%m/%d')
            if birthdate.date() > datetime.now().date():
                return invalidParameter("birthdate")
        except KeyError:
            return missingParameterInJson("birthdate")
        except ValueError:
            return invalidParameter("birthdate")
        
        
        
        data = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "birthdate": birthdate,
            "created_date" : datetime.utcnow().replace(microsecond=0).isoformat()
        }
        
        if createNewUser(data):
            return creationSucces()
        else:
            return creationFail()
        
        
        