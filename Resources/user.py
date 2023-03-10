from flask_restful import Resource


class User(Resource):
    def get(self):
        return {'message': 'User not found'}, 200
