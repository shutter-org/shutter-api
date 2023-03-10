from .App import *
from flask import Flask
from flask_restful import Api


def start() -> None:
    """
    start Server
    """
    app = Flask(__name__)
    api = Api(app)
    
    addConfig(app)
    addRouters(app)
    
    app.run()

