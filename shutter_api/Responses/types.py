from flask import jsonify

def ok(data=None) -> tuple:
    if data is None:
        return "",200
    else:
        return jsonify(data),200

def creationSucces(data=None) -> tuple:
    if data is None:
        return "",201
    else:
        return jsonify(data),201

def creationFail() -> tuple:
    return jsonify({
        "Error": "Creation failure",
        "Code":500
        }),500

def deleteSucces() -> tuple:
    return "ok",200

def deleteFail() -> tuple:
    return jsonify({
        "Error": "delete failure",
        "Code": 500
        }),500
    
def noAcces() -> tuple:
    return "No acces",403
    
def requestFail() -> tuple:
     return jsonify({
        "Error": "request failure",
        "Code":500
        }),500

def invalidParameter(param:str) -> tuple:
    return jsonify({
        "Error": f"Invalid param '{param}'",
        "Code":400
        }),400

def missingParameter(param:str) -> tuple:
    return jsonify({
        "Error": f"Missing param '{param}'",
        "Code":400
        }),400

def missingParameterInJson(param:str) -> tuple:
    return jsonify({
        "Error": f"Missing param in Json '{param}'",
        "Code":400
        }),400
    
def connectionSucces(token:str, user:dict) -> tuple:
    data = {
        "acces_token": token,
        "user": user
    }
    return jsonify(data),200

def connectionFail() -> tuple:
    return jsonify({"Error": "connection failure"}), 401
