from flask import request, jsonify
import uuid
from datetime import datetime

class PublicationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def publication(app) -> None:
    
    @app.route("/publications", methods=["GET"])
    def getPublication():
        tag = request.args.get('tag')
        return f"get publication with tag : {tag}"
    
    @app.route("/publications", methods=["POST"])
    def postPublication():
        
        data = request.get_json()
        try:
            description = data["description"]
            username = data["username"]
            picture = data["picture"]
            
            if description == "":
                raise PublicationError("description param invalid")
            elif username == "":
                raise PublicationError("username param invalid")
            elif picture == "":
                raise PublicationError("picture param invalid")
                
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "username" : username,
            "publication_id": uuid.uuid4(),
            "description" : description,
            "created_date" :  datetime.utcnow().replace(microsecond=0).isoformat(),
            "picture" : picture
        }
        
        return jsonify(data),200
    
    @app.route("/publications/<publication_id>/comments", methods=["POST"])
    def postcommentPublication(publication_id):
        
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
            "username" : username,
            "comment_id":  uuid.uuid4(),
            "publication_id": publication_id,
            "message" : message,
            "created_date" :  datetime.utcnow().replace(microsecond=0).isoformat()
        }
        
        return jsonify(data),200
    
    
    
    @app.route("/publications/<publication_id>/like", methods=["POST"])
    def postLikePublication(publication_id):
        
        data = request.get_json()
        try:
            like = data["like"]
            if type(like) is not bool:
                raise PublicationError("like is not of boolean type")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except PublicationError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "like": like,
            "publication_id": publication_id
        }
        
        return jsonify(data),200
    
    