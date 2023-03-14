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
        try:
            tag = request.args.get('tag')
        except ValueError:
            tag = []
        try:
            username = request.args.get('username')
        except ValueError:
            username = None
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        
        if tag == []:
            data = getPublications(username=username, offset=page)
        else:
            data = getPublicationsFromTag(tag=tag,username=username,offset=page)
            
        if data is None:
            return jsonify({"Error": f"No publication for tag '{tag}'"}),400
        else:
            return jsonify(data),200
        
    
    @app.route("/publications", methods=["POST"])
    def post_publications():
        
        data = request.get_json()
        try:
            description = data["description"]
            username = data["username"]
            picture = data["picture"]
            try:
                tags = data["tags"]
            except KeyError:
                tags = []
            
            if description == "":
                raise PublicationError("description param invalid")
            elif username == "" or not doesUsernameExist(username):
                raise PublicationError("username param invalid")
            elif picture == "":
                raise PublicationError("picture param invalid")
            elif type(tags) != list:
                raise PublicationError("tags is not an array")
                
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        for tag in tags:
            if type(tag) != str:
                return jsonify({"Error": f"one of tag is not a string"}), 400
            if not doesTagExist(tag):
                if not createTag(tag):
                    return jsonify({"Error": f"tag '{tag}' is not a valid tag"}), 400
                
        data = {
            "poster_username" : username,
            "publication_id": uuid.uuid4(),
            "description" : description,
            "created_date" :  datetime.utcnow().isoformat(),
            "picture" : picture,
        }
        if createPublication(data):
            for tag in tags:
                addTagToPublication(tag, data["publication_id"])
            return jsonify({"publication_id": data["publication_id"]}), 201
        else:
            return jsonify({"creation status": "Fail"}), 400
        
    @app.route("/publications/<publication_id>", methods=["GET"])
    def get_publication_publicationId(publication_id):
        
        try:
            username = request.args.get('username')
            if not doesUsernameExist(username):
                username = None
        except ValueError:
            username = None
        
        data = getPublicationById(publication_id, username=username)
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
            username = request.args.get('username')
        except ValueError:
            username = None
            
        try:
            page = int(request.args.get('page'))
            
        except (ValueError,TypeError):
            page = 1
            
        if publication_id == "" or not doesPublicationExist(publication_id):
            return jsonify({'error': "publication param invalid"}), 400
        
        if page < 1:
            return jsonify({'error': "page param invalid"}), 400
            
        if username is not None and not doesUsernameExist(username):
            return jsonify({'error': "username param invalid"}), 400


        
        data = getCommentsOfPublication(publication_id, username=username, offset=page)
        if data is None:
            return jsonify({'error': "bad request"}), 400
        else:
            return jsonify({"publication_comments": data}),200
    
    