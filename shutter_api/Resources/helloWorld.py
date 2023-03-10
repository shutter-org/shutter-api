from flask_restful import Resource
from shutter_api.config import mysql
from flask import jsonify


class HelloWorld(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cmd = "select * from Transactions;"
            cursor.execute(cmd)

            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            return jsonify(json_data)
        except Exception as e:
            print(e)
        finally:
            conn.close()
            cursor.close()
