from datetime import timedelta

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from shutter_api import MYSQL
from shutter_api.Keys import SQL_KEY, JWT_KEY


def addConfig(app) -> None:
    """
    setup config for MySQL
    """
    CORS(app)
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        user_id = jwt_data["sub"]
        return user_id

    app.config['MYSQL_DATABASE_USER'] = 'admin'
    app.config['MYSQL_DATABASE_PASSWORD'] = SQL_KEY
    app.config['MYSQL_DATABASE_DB'] = 'shutter'
    app.config['MYSQL_DATABASE_HOST'] = 'shutter-db-13.cqw2hvrmj4z8.us-east-1.rds.amazonaws.com'
    app.config['JWT_SECRET_KEY'] = JWT_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    MYSQL.init_app(app)
