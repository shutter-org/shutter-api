from flask import jsonify, request
from datetime import datetime

class SighUnError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def signUp(app) -> None:
    
    @app.route("/signup", methods=["POST"])
    def postSignUp():
        
        data = request.get_json()
        try:
            userName = data["username"]
            password = data["password"]
            email = data["email"]
            name = data["name"]
            birthdate = data["birthdate"]
            bio = data["bio"]
            
            if userName == "":
                raise SighUnError("invalid username")
            elif password == "":
                raise SighUnError("invalid password")
            elif email == "":
                raise SighUnError("invalid email")
            elif name == "":
                raise SighUnError("invalid name")
            elif birthdate == "":
                raise SighUnError("invalid birthdate")
            elif bio == "":
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
        
        return jsonify(data),200