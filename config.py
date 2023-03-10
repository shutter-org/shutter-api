from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'tests'
app.config['MYSQL_DATABASE_HOST'] = 'database-1.cqw2hvrmj4z8.us-east-1.rds.amazonaws.com'
mysql.init_app(app)