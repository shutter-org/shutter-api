from shutter_api import MYSQL
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import secrets




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
    app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
    app.config['MYSQL_DATABASE_DB'] = 'shutter'
    app.config['MYSQL_DATABASE_HOST'] = 'shutter-db.cqw2hvrmj4z8.us-east-1.rds.amazonaws.com'
    app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
    MYSQL.init_app(app)
    
    
