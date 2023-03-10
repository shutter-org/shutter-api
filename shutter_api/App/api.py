from shutter_api.Resources import *

def addResources(api) -> None:
    api.add_resource(HelloWorld, '/')
    api.add_resource(User, '/user')