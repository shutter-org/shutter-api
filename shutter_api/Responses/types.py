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
        return jsonify({"msg": "ok"}), 200
    else:
        return jsonify(data), 200


def creationSucces(data=None) -> tuple:
    """
    creation success response with code 201

    Args:
        data (_type_, optional): data that is sent. Defaults to None.

    Returns:
        tuple: response, 201
    """
    if data is None:
        return jsonify({"msg": "ok"}), 201
    else:
        return jsonify(data), 201


def creationFail() -> tuple:
    """
    creation fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "Creation failure",
        "Code": 500
    }), 500


def deleteSucces() -> tuple:
    """
    delete Success code 200

    Returns:
        tuple: response, 200
    """
    return jsonify({"msg": "ok"}), 200


def deleteFail() -> tuple:
    """
    Delete fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "delete failure",
        "Code": 500
    }), 500


def noAcces() -> tuple:
    """
    No access response, code 403

    Returns:
        tuple : response, 403
    """
    return jsonify({"msg": "no acces"}), 403


def requestFail() -> tuple:
    """
    Request fail internal error, code 500

    Returns:
        tuple: response, 500
    """
    return jsonify({
        "Error": "request failure",
        "Code": 500
    }), 500


def invalidParameter(param: str) -> tuple:
    """invalid parameter response

    Args:
        param (str): the name of the param

    Returns:
        tuple: response, 400
    """
    return jsonify({
        "Error": f"Invalid param '{param}'",
        "Code": 400
    }), 400


def missingParameter(param: str) -> tuple:
    """missing parameter

    Args:
        param (str): parameter name

    Returns:
        tuple: response, 400
    """
    return jsonify({
        "Error": f"Missing param '{param}'",
        "Code": 400
    }), 400


def missingParameterInJson(param: str) -> tuple:
    """Missing param in json

    Args:
        param (str): parameter name

    Returns:
        tuple: response, 400
    """
    return jsonify({
        "Error": f"Missing param in Json '{param}'",
        "Code": 400
    }), 400


def connectionSucces(token: str, user: dict) -> tuple:
    """
    connection success response, code 200

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
    return jsonify(data), 200


def connectionFail() -> tuple:
    """
    Connection fail response

    Returns:
        tuple: response, 401
    """
    return jsonify({"Error": "connection failure"}), 401
