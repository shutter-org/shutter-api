from flask import jsonify

def ok(data=None) -> tuple:
    if data is None:
        return "ok",200
    else:
        return jsonify(data),200

def creationSucces(data=None) -> tuple:
    if data is None:
        return "ok",201
    else:
        return jsonify(data),201

def creationFail() -> tuple:
    return jsonify({
        "Error": "Creation fail",
        "Code":422
        }),422

def deleteSucces() -> tuple:
    return "ok",200

def deleteFail() -> tuple:
    return jsonify({
        "Error": "delete fail",
        "Code":422
        }),422
    
def noAcces() -> tuple:
    return "No acces",403
    
def requestFail() -> tuple:
     return jsonify({
        "Error": "request fail",
        "Code":422
        }),422

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
    
def connectionSucces() -> tuple:
    return "connection succes",200

def connectionFail() -> tuple:
    return "connection fail", 401