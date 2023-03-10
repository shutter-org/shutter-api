from flask import request, Response
import uuid

def publication(app) -> None:
    
    @app.route("/publications", methods=["GET"])
    def getPublication():
        tag = request.args.get('tag')
        return f"get publication with tag : {tag}"
    
    @app.route("/publications", methods=["POST"])
    def postPublication():
        return str(uuid.uuid4())
    
    @app.route("/publications/<publication_id>/comments", methods=["POST"])
    def postcommentPublication(publication_id):
        return f"comment if {uuid.uuid4()} publicaiton with id : {publication_id}"
    
    @app.route("/publications/<publication_id>/like", methods=["POST"])
    def postLikePublication(publication_id):
        return f"like publicaiton with id : {publication_id}"
    
    