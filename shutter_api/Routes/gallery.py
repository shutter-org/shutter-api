from flask import request, jsonify
import uuid
from datetime import datetime
from shutter_api.MySQL_command import *
from shutter_api.Responses import *

class GalleryError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def gallery(app) -> None:
    
    @app.route("/gallerys", methods=["Post"])
    def post_gallerys():
        data = request.get_json()
        
        try:
            username = data["username"]
            if type(username) is not str:
                return invalidParameter("username")
            username = username.strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except KeyError:
            return missingParameterInJson("username")
        
        try:
            description = data["description"]
            if type(description) is not str:
                return invalidParameter("description")
            description = description.strip()
            if description == "":
                return invalidParameter("description")
        except KeyError:
            return missingParameterInJson("description")
        
        try:
            private = data["private"]
            if type(private) is not bool:
                return invalidParameter("private")
        except KeyError:
            return missingParameterInJson("private")

        
        data = {
            "gallery_id": uuid.uuid4(),
            "description":description,
            "private":int(private),
            "creator_username": username,
            "created_date": datetime.utcnow().isoformat()
        }
        
        if createGallery(data):
            return creationSucces({"gallery_id": data["gallery_id"]})
        else:
            return creationFail()
        
    
    @app.route("/gallerys/<gallery_id>", methods=["Post"])
    def post_gallerys_galleryId(gallery_id):
        data = request.get_json()
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        try:
            publication_id = data["publication_id"]
            if type(publication_id) is not str:
                return invalidParameter("publication_id")
            publication_id = publication_id.strip()
            if not doesPublicationExist(publication_id):
                return invalidParameter("publication_id")
        except KeyError:
            return missingParameterInJson("publication_id")
       
        
        data = {
            "publication_id": publication_id,
            "gallery_id": gallery_id
        }
        
        if addPublicationToGallery(data):
            return ok()
        else:
            return requestFail()
        

    
    @app.route("/gallerys/<gallery_id>/like", methods=["Post"])
    def post_gallerys_galleryId_like(gallery_id):
        data = request.get_json()
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")
        
        try:
            username = data["username"]
            if type(username) is not str:
                return invalidParameter("username")
            username = username.strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except KeyError:
            return missingParameterInJson("username")
        
        
        data = {
            "rating": int(rating),
            "gallery_id": gallery_id,
            "username": username
        }
        
        if likeGallery(data):
            return jsonify({"status": "succes"}), 200
        else:
            return jsonify({"status": "Fail"}), 400
        
    @app.route("/gallerys/<gallery_id>", methods=["DELETE"])
    def delete_gallerys_galleryId(gallery_id):

        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        if deleteGalleryFromDB(gallery_id):
            return deleteSucces()
        else:
            return deleteFail()
        
    @app.route("/gallerys/<gallery_id>", methods=["GET"])
    def get_gallerys_galleryId(gallery_id):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        try:
            username = request.args.get('username').strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except ValueError:
            return missingParameter("username")


        data = getGalleryById(gallery_id, username)
        
        if data is None:
            return noAcces()
        else:
            return ok(data=data)
        
    @app.route("/gallerys/<gallery_id>/publications", methods=["GET"])
    def get_gallerys_galleryId_publications(gallery_id):
        
        try:
            username = request.args.get('username').strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except ValueError:
            return missingParameter("username")
            
        try:
            page = int(request.args.get('page'))
            if page < 1: 
                return invalidParameter("page")
        except ValueError:
            page = 1
        except TypeError:
            return invalidParameter("page")

        data = getGalleryPublications(gallery_id, username=username,offset=page)
        if data is None:
            return noAcces()
        else:
            return ok(data=data)