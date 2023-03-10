def home(app) -> None:
    
    @app.route("/", methods=["GET"])
    def getHome():
        return "Home Page"  