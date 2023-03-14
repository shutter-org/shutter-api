from shutter_api.MySQL_command.home import command
def home(app) -> None:
    
    @app.route("/", methods=["GET"])
    def get_home():
        command()
        return "Home Page"  