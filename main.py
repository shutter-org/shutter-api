from Resources.helloWorld import HelloWorld
from Resources.user import User
from app import app
from app import api

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True)
