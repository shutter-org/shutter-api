from flask import request, jsonify
import uuid

from datetime import datetime
from shutter_api.MySQL_command import *

class PublicationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def publication(app) -> None:
    
    @app.route("/publications", methods=["GET"])
    def get_publications():
        tag = request.args.get('tag')
        return f"get publication with tag : {tag}"
    
    @app.route("/publications", methods=["POST"])
    def post_publications():
        
        data = request.get_json()
        try:
            description = data["description"]
            username = data["username"]
            picture = data["picture"]
            
            if description == "":
                raise PublicationError("description param invalid")
            elif username == "" or not doesUsernameExist(username):
                raise PublicationError("username param invalid")
            elif picture == "":
                raise PublicationError("picture param invalid")
                
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "poster_username" : username,
            "publication_id": uuid.uuid4(),
            "description" : description,
            "created_date" :  datetime.utcnow().isoformat(),
            "picture" : picture
        }
        if createPublication(data):
            return jsonify({"publication_id": data["publication_id"]}), 201
        else:
            return jsonify({"creation status": "Fail"}), 400
        
    @app.route("/publications/<publication_id>", methods=["GET"])
    def get_publication_publicationId(publication_id):
        
        data = getPublicationById(publication_id)
        if data is None:
            return jsonify({"Error": "publication_id does not exist"}),400
        else:
            return jsonify(data),200
    
    @app.route("/publications/<publication_id>/comments", methods=["POST"])
    def post_publications_publicationId_comments(publication_id):
        
        data = request.get_json()
        try:
            message = data["message"]
            username = data["username"]
            if message == "":
                raise PublicationError("message param invalid")
            elif username == "":
                raise PublicationError("username param invalid")
                
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        
        data = {
            "commenter_username" : username,
            "comment_id":  uuid.uuid4(),
            "publication_id": publication_id,
            "message" : message,
            "created_date" :  datetime.utcnow().isoformat()
        }
        

        if createComment(data):
            return jsonify({"comment_id": data["comment_id"]}), 201
        else:
            return jsonify({"creation status": "Fail"}), 400
    
    
    
    @app.route("/publications/<publication_id>/like", methods=["POST"])
    def post_publication_publicationId_like(publication_id):
        
        data = request.get_json()
        try:
            rating = data["rating"]
            username = data["username"]
            if username == "":
                raise PublicationError("username param invalid")
            if type(rating) is not bool:
                raise PublicationError("rating is not of boolean type")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "rating": str(int(rating)),
            "publication_id": publication_id,
            "username": username
        }
        
        if likePublication(data):
            return jsonify({"status": "succes"}), 200
        else:
            return jsonify({"status": "Fail"}), 400

    
    @app.route("/publications/<publication_id>", methods=["DELETE"])
    def delete_publication_publicationId(publication_id):
        
        if deletePublicationFromDB(publication_id):
            return jsonify({"deleted status": "succes"}),200
        else:
            return jsonify({"deleted status": "fail"}),400
        
    @app.route("/publications/<publication_id>/comments", methods=["GET"])
    def get_publication_publicationId_comments(publication_id):
        
        
        try:
            if publication_id == "" or not doesPublicationExist(publication_id):
                raise PublicationError("publication oaram invalid")
            data = request.get_json()
            username = data["username"]
            if username == "" or not doesUsernameExist(username):
                raise PublicationError("username param invalid")
            
            
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        except Exception as e:
            username = None
        
        data = getCommentsOfPublication(publication_id, username = username)
        if data is None:
            return jsonify({'error': "bad request"}), 400
        else:
            return jsonify({"publication_comments": data}),200
    
    