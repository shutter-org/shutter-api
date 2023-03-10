from flask import request, jsonify
import uuid

class GalleryError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def gallery(app) -> None:
    
    @app.route("/gallery", methods=["Post"])
    def postCreateGallery():
        data = request.get_json()
        try:
            username = data["username"]
            title = data["title"]
            description = data["description"]
            private = data["private"]
            
            if username == "":
                raise GalleryError("username param invalid")
            if title == "":
                raise GalleryError("title param invalid")
            if description == "":
                raise GalleryError("description param invalid")
            if type(private) is not bool:
                raise GalleryError("private is not bool")
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "gallery_id": uuid.uuid4(),
            "title": title,
            "description":description,
            "private":private,
            "username":username
        }
        
        return jsonify(data),200
    
    @app.route("/gallery/<gallery_id>", methods=["Post"])
    def postAddPublicationTogallery(gallery_id):
        data = request.get_json()
        try:
            publication_id = data["publication_id"]
            
            if publication_id == "":
                raise GalleryError("publication_id param invalid")
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "publication_id": publication_id,
            "gallery_id": gallery_id
        }
        
        return jsonify(data), 200

    
    @app.route("/gallery/<gallery_id>/like", methods=["Post"])
    def postLikegallery(gallery_id):
        data = request.get_json()
        try:
            like = data["like"]
            if type(like) is not bool:
                raise GalleryError("like is not of boolean type")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "like": like,
            "gallery_id": gallery_id
        }
        
        return jsonify(data), 200
        
    
    @app.route("/gallery/<gallery_id>", methods=["GET"])
    def getGalleryFromId(gallery_id):
        return f"get gallery with id : {gallery_id}"