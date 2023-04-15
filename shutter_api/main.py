from flask import Flask

from .App import *


def start() -> None:
    """
    start Server
    """
    app = Flask(__name__)

    addConfig(app)
    addRouters(app)

    app.run()
