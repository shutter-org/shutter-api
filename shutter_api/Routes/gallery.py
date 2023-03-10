def gallery(app) -> None:
    
    @app.route("/gallery/<gallery_id>", methods=["Post"])
    def postAddPublicationTogallery(gallery_id):
        return f"add publication to gallery with id : {gallery_id}"
    
    @app.route("/gallery/<gallery_id>/like", methods=["Post"])
    def postLikegallery(gallery_id):
        return f"like gallery with id : {gallery_id}"
    
    @app.route("/gallery/<gallery_id>", methods=["GET"])
    def getGalleryFromId(gallery_id):
        return f"get gallery with id : {gallery_id}"