import uuid

def signUp(app) -> None:
    
    @app.route("/signup", methods=["POST"])
    def postSignUp():
        return str(uuid.uuid4())