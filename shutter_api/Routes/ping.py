from flask import request
from flask_jwt_extended import jwt_required, get_current_user
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def ping(app) -> None:

    @app.route("/ping", methods=["GET"])
    @jwt_required()
    def get_ping():
        return ok()