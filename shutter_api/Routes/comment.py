
def comment(app) -> None:
    
    @app.route("/comment/<comment>/like", methods=["Post"])
    def postLikeComment(comment):
        return f"like comment with id : {comment}"