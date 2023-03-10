def signIn(app) -> None:
    
    @app.route("/signin", methods=["GET"])
    def getSignIn():
        return "signIn Page"