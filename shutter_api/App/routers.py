from shutter_api.Routes import *

def addRouters(app):
    """
    add All routers to app
    """
    signUp(app)
    signIn(app)
    user(app)
    publication(app)
    comment(app)
    gallery(app)
    tag(app)
