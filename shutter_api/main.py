from shutter_api.App import *
from flask import Flask

def start() -> None:
    """
    start Server
    """
    app = Flask(__name__)
    
    addConfig(app)
    addRouters(app)
    
    app.run()
    


