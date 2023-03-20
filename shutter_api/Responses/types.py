from flask import jsonify

def ok(data=None) -> tuple:
    """
    ok response with code 200

    Args:
        data (_type_, optional): data that are being send. Defaults to None.

    Returns:
        tuple: response, 200
    """
    if data is None:
        return jsonify({"msg":"ok"}),200
    else:
        return jsonify(data),200

def creationSucces(data=None) -> tuple:
    """
    creation succes reponse with code 201

    Args:
        data (_type_, optional): data that is send. Defaults to None.

    Returns:
        tuple: response, 201
    """
    if data is None:
        return jsonify({"msg":"ok"}),201
    else:
        return jsonify(data),201

def creationFail() -> tuple:
    """
    creation fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "Creation failure",
        "Code":500
        }),500

def deleteSucces() -> tuple:
    """
    delete Succes code 200

    Returns:
        tuple: response, 200
    """
    return jsonify({"msg":"ok"}),200

def deleteFail() -> tuple:
    """
    Delet fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "delete failure",
        "Code": 500
        }),500
    
def noAcces() -> tuple:
    """
    no acces response, code 403

    Returns:
        tuple: reponse, 403
    """
    return jsonify({"msg":"no acces"}),403
    
def requestFail() -> tuple:
    """
    request fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "request failure",
        "Code":500
        }),500

def invalidParameter(param:str) -> tuple:
    """invalid parmeter reponse

    Args:
        param (str): the name of the param

    Returns:
        tuple: reponse, 400
    """
    return jsonify({
        "Error": f"Invalid param '{param}'",
        "Code":400
        }),400

def missingParameter(param:str) -> tuple:
    """missing parameter

    Args:
        param (str): parameter name

    Returns:
        tuple: reponse, 400
    """
    return jsonify({
        "Error": f"Missing param '{param}'",
        "Code":400
        }),400

def missingParameterInJson(param:str) -> tuple:
    """Missing param in json

    Args:
        param (str): parameter name

    Returns:
        tuple: reponse, 400
    """
    return jsonify({
        "Error": f"Missing param in Json '{param}'",
        "Code":400
        }),400
    
def connectionSucces(token:str, user:dict) -> tuple:
    """
    connection succes reponse, code 200

    Args:
        token (str): access token
        user (dict): username and user picture

    Returns:
        tuple: response, 200
    """
    data = {
        "access_token": token,
        "user": user
    }
    return jsonify(data),200

def connectionFail() -> tuple:
    """
    connection fail response

    Returns:
        tuple: reponse, 401
    """
    return jsonify({"Error": "connection failure"}), 401
