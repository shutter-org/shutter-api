from flask import request
from flask_jwt_extended import jwt_required

from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def tag(app) -> None:
    @app.route("/tags", methods=["GET"])
    @jwt_required()
    def get_tags():

        try:
            search = request.args.get('search', default="", type=str)
        except ValueError:
            search = ""

        data = getTags(search)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
