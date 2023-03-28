from shutter_api.App import *
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Ok'

addConfig(app)
addRouters(app)

