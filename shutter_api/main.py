from .App import *
from flask import Flask
from flask_cors import CORS


def start() -> None:
    """
    start Server
    """
    app = Flask(__name__)
    CORS(app)
    
    addConfig(app)
    addRouters(app)
    
    app.run()
    


