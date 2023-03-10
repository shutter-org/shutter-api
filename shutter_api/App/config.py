from shutter_api import MYSQL


def addConfig(app) -> None:
    """
    setup config for MySQL
    """

    app.config['MYSQL_DATABASE_USER'] = 'admin'
    app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
    app.config['MYSQL_DATABASE_DB'] = 'shutter'
    app.config['MYSQL_DATABASE_HOST'] = 'shutter-db.cqw2hvrmj4z8.us-east-1.rds.amazonaws.com'
    MYSQL.init_app(app)
