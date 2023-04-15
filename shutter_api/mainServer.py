from flask import Flask

from .App import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Ok'


addConfig(app)
addRouters(app)
