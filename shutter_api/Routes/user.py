def user(app) -> None:
    
    @app.route("/users/<username>", methods=["GET"])
    def getUser(username):
        return username
    
    @app.route("/users/<username>/followed/publications", methods=["GET"])
    def getUserFollowedPublications(username):
        return username + " Followed publication"