def home(app) -> None:
    
    @app.route("/", methods=["GET"])
    def get_home():
        return "Home Page"  