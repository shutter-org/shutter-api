
from .Resources import *
from shutter_api import app


def start():
    app.api.add_resource(HelloWorld, '/')
    app.api.add_resource(User, '/user')
    
    app.app.run()

