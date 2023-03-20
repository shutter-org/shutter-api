from flask import request
import uuid
import re

from datetime import datetime
from shutter_api.MySQL_command import *
from shutter_api.Responses import *
from flask_jwt_extended import jwt_required, get_current_user


def publication(app) -> None:
    
    @app.route("/publications", methods=["GET"])
    @jwt_required()
    def get_publications():
        
        username = get_current_user()
        
        try:
            tag = request.args.get('tag',default=None,type=str)
            if tag == "":
                pass
            elif tag is not None:
                if not doesTagExist(tag):
                    return invalidParameter("tag")
        except ValueError:
            tag = None
            
        try:
            page = request.args.get('page', default=1, type=int)

            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")

        data = {}
        

        if tag is None or tag == "":
            data["publications"] = getPublications(username=username, offset=page)
            data["nb_publication"] = getNbPublications()
        else:
            data["publications"] = getPublicationsFromTag(tag=tag,username=username,offset=page)
            data["nb_publication"] = getNbpublicationFromTag(tag)
                
            
        if data["publications"] is None or data["nb_publication"] is None:
            return requestFail()
        else:
            return ok(data=data)
          
    @app.route("/publications", methods=["POST"])
    @jwt_required()
    def post_publications():
        
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
            picture = data["picture"]
            if type(picture) is not str:
                return invalidParameter("picture")
            if bool(re.match('^[01]*$', picture)):
                return invalidParameter("picture")
        except KeyError:
            return missingParameterInJson("picture")
        
        try:
            tags = data["tags"]
            if type(tags) != list:
                return invalidParameter("tags")  
        except KeyError:
            return missingParameterInJson("tags")

        for tag in tags:
            if type(tag) is not str and tag == "":
                return invalidParameter("tags")
                
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
            return creationSucces(data={"publication_id": data["publication_id"]})
        else:
            return creationFail()
        
    @app.route("/publications/<publication_id>", methods=["GET"])
    @jwt_required()
    def get_publication_publicationId(publication_id:str):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()
        
        data = getPublicationById(publication_id, username=username)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
        
    @app.route("/publications/<publication_id>", methods=["PUT"])
    @jwt_required()
    def put_publication_publicationId(publication_id:str):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        data = request.get_json()
        username = get_current_user()
        if not doesPublicationBelongToUser(username, publication_id):
            return noAcces()
        
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
            tags = data["tags"]
            if type(tags) != list:
                return invalidParameter("tags")  
        except KeyError:
            tags = None
        
        if description is None and tags is None:
            missingParameterInJson("tags, description")
        
        if tags is not None:
            for tag in tags:
                if type(tag) is not str:
                    return invalidParameter("tags")
            
            if not removeTagsFromPublication(publication_id):
                requestFail()
                
            for tag in tags:
                if not addTagToPublication(tag, publication_id):
                    requestFail()
                
        if description is not None:
            if not updatepublication(publication_id, description):
              return requestFail()
          
        return ok()
        
    @app.route("/publications/<publication_id>", methods=["DELETE"])
    @jwt_required()
    def delete_publication_publicationId(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()

        if not isUsernameCreatorOfPublication(username, publication_id):
            return noAcces()
        
        
        if deletePublicationFromDB(publication_id):
            return deleteSucces()
        else:
            return deleteFail()
             
    @app.route("/publications/<publication_id>/comments", methods=["GET"])
    @jwt_required()
    def get_publication_publicationId_comments(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()
            
        try:
            page = request.args.get('page', default=1, type=int)
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            return invalidParameter("page")
            
        
        data = getCommentsOfPublication(publication_id, username=username, offset=page)
        if data is None:
            return requestFail
        else:
            return ok(data=data)
            
    @app.route("/publications/<publication_id>/comments", methods=["POST"])
    @jwt_required()
    def post_publications_publicationId_comments(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()
        data = request.get_json()
        
        try:
            message = data["message"]
            if type(message) is not str:
                return invalidParameter("message")
            message = message.strip()
            if message == "":
                return invalidParameter("message")
        except KeyError:
            return missingParameterInJson(message)

        
        data = {
            "commenter_username" : username,
            "comment_id":  uuid.uuid4(),
            "publication_id": publication_id,
            "message" : message,
            "created_date" :  datetime.utcnow().isoformat()
        }
        

        if createComment(data):
            return creationSucces(data={"comment_id": data["comment_id"]})
        else:
            return creationFail()
     
    @app.route("/publications/<publication_id>/like", methods=["POST"])
    @jwt_required()
    def post_publication_publicationId_like(publication_id:str):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()
        data = request.get_json()
        
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                return invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")
        
        if likePublication(publication_id,username, int(rating)):
            return ok()
        else:
            return requestFail()

    @app.route("/publications/<publication_id>/like", methods=["PUT"])
    @jwt_required()
    def put_publication_publicationId_like(publication_id:str):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()
        
        data = request.get_json()
        try:
            rating = data["rating"]
            if type(rating) is not bool:
                invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")

        print(publication_id,username)
        if not didUserRatePublication(publication_id,username):
            return noAcces()
            
        if updateLikePublication(publication_id, username, rating):
            return ok()
        else:
            return requestFail()
        
    @app.route("/publications/<publication_id>/like", methods=["DELETE"])
    @jwt_required()
    def delete_publication_publicationId_like(publication_id:str):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter("publication_id")
        
        username = get_current_user()

        if not didUserRatePublication(publication_id,username):
            return noAcces()
            
        
        if deleteLikePublication(publication_id, username):
            return deleteSucces()
        else:
            return deleteFail()
    
        
    
    
    