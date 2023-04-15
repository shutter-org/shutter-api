from flask_jwt_extended import jwt_required

from shutter_api.Responses import *


def ping(app) -> None:
    @app.route("/ping", methods=["GET"])
    @jwt_required()
    def get_ping():
        return ok()
