
from .App import *
from flask import Flask
from flask_restful import Api


def start():
    app = Flask(__name__)
    api = Api(app)
    
    addConfig(app)
    addResources(api)
    
    app.run()

