from flask import request, jsonify

class SighInError(Exception):
    pass

def signIn(app) -> None:
    
    @app.route("/signin", methods=["GET"])
    def getSignIn():
        data = request.get_json()
        try:
            userName = data["username"]
            password = data["password"]
            
            if userName == "" or password == "":
                raise SighInError()
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except SighInError:
            return jsonify({'Invalid': "userName or Password invalid"}), 400

        data = {
            "username": userName,
            "password": password
        }
        
        return jsonify(data), 200