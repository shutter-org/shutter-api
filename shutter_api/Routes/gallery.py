from flask import request
from flask_jwt_extended import jwt_required, get_current_user
import uuid
from datetime import datetime
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def gallery(app) -> None:
    
    @app.route("/gallerys", methods=["Post"])
    @jwt_required()
    def post_gallerys():
        data = request.get_json()
        
        username = get_current_user()
        
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
            title = data["title"]
            if type(title) is not str:
                return invalidParameter("title")
            title = title.strip()
            if title == "":
                return invalidParameter("title")
        except KeyError:
            return missingParameterInJson("title")
        
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
            "title": title,
            "created_date": datetime.utcnow().isoformat()
        }
        
        if createGallery(data):
            return creationSucces({"gallery_id": data["gallery_id"]})
        else:
            return creationFail()
        
    @app.route("/gallerys/<gallery_id>", methods=["GET"])
    @jwt_required()
    def get_gallerys_galleryId(gallery_id):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        
        username = get_current_user()

        if not doesUserHasAccesToGallery(username,gallery_id):
            return noAcces()

        data = getGalleryById(gallery_id, username)
        
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
        
    @app.route("/gallerys/<gallery_id>", methods=["PUT"])
    @jwt_required()
    def put_gallerys_galleryId(gallery_id):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        
        if not doesGalleryBelongToUser(username):
            return noAcces()
        
        data = request.get_json()
        
        try:
            description = data["description"]
            if type(description) is not str:
                return invalidParameter("description")
            description = description.strip()
            if description == "":
                return invalidParameter("description")
        except KeyError:
            description = None
            
        try:
            title = data["title"]
            if type(title) is not str:
                return invalidParameter("title")
            title = title.strip()
            if title == "":
                return invalidParameter("title")
        except KeyError:
            title = None
            
        try:
            private = data["private"]
            if type(private) is not bool:
                return invalidParameter("private")
        except KeyError:
            private = None
            
        if private is None and title is None and description is None:
            return missingParameterInJson("private, title, description")
        
        
        if updateGallery(gallery_id, description=description, title=title, private=private):
            return ok()
        else:
            return requestFail()
        
    @app.route("/gallerys/<gallery_id>", methods=["DELETE"])
    @jwt_required()
    def delete_gallerys_galleryId(gallery_id):

        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        if not doesGalleryBelongToUser(username,gallery_id):
            return noAcces()
        
        if deleteGalleryFromDB(gallery_id):
            return deleteSucces()
        else:
            return deleteFail()
        
    @app.route("/gallerys/<gallery_id>/publications", methods=["GET"])
    @jwt_required()
    def get_gallerys_galleryId_publications(gallery_id):
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        
        if not doesUserHasAccesToGallery(username,gallery_id):
            return noAcces()
            
        try:
            page = request.args.get('page', default=1, type=int)

            if page < 1: 
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")

            

        data = getGalleryPublications(gallery_id, username=username,offset=page)
        if data is None:
            return noAcces()
        else:
            return ok(data=data)
        
    @app.route("/gallerys/<gallery_id>/publications", methods=["Post"])
    @jwt_required()
    def post_gallerys_galleryId_publication(gallery_id):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        data = request.get_json()
        try:
            publication_id = data["publication_id"]
            if type(publication_id) is not str:
                return invalidParameter("publication_id")
            publication_id = publication_id.strip()
            if not doesPublicationExist(publication_id):
                return invalidParameter("publication_id")
        except KeyError:
            return missingParameterInJson("publication_id")
        
        username = get_current_user()
        if not doesGalleryBelongToUser(username, gallery_id):
            return noAcces()
        
        if addPublicationToGallery(gallery_id, publication_id):
            return ok()
        else:
            return requestFail()
        
    @app.route("/gallerys/<gallery_id>/publications", methods=["DELETE"])
    @jwt_required()
    def delete_gallerys_galleryId_publication(gallery_id):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        if not doesGalleryBelongToUser(username, gallery_id):
            return noAcces()
        
        data = request.get_json()
        try:
            publication_id = data["publication_id"]
            if type(publication_id) is not str:
                return invalidParameter("publication_id")
            publication_id = publication_id.strip()
            if not doesPublicationExist(publication_id):
                return invalidParameter("publication_id")
        except KeyError:
            return missingParameterInJson("publication_id")
        
        
        if removePublicationFromGallery(gallery_id, publication_id):
            return ok()
        else:
            return requestFail()
        
        
    @app.route("/gallerys/<gallery_id>/like", methods=["Post"])
    @jwt_required()
    def post_gallerys_galleryId_like(gallery_id:str):
        data = request.get_json()
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        
        if not doesUserHasAccesToGallery(username,gallery_id):
            return noAcces()
        
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                return invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")
        
        
        if likeGallery(gallery_id,username,int(rating)):
            return ok()
        else:
            return requestFail()
        
    @app.route("/gallerys/<gallery_id>/like", methods=["PUT"])
    @jwt_required()
    def put_gallerys_galleryId_like(gallery_id:str):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()
        
        data = request.get_json()
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")

        if not didUserRateGallery(gallery_id, username):
            return noAcces()
            
        if updateLikeGallery(gallery_id, username, rating):
            return ok()
        else:
            return requestFail()
        
    @app.route("/gallerys/<gallery_id>/like", methods=["DELETE"])
    @jwt_required()
    def delete_gallerys_galleryId_like(gallery_id:str):
        
        if not doesGalleryExist(gallery_id):
            return invalidParameter("gallery_id")
        
        username = get_current_user()

        if not didUserRateGallery(gallery_id, username):
            return noAcces()
            
        
        if deleteLikeGallery(gallery_id, username):
            return deleteSucces()
        else:
            return deleteFail()
        
