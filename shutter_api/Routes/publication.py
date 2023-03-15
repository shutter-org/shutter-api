from flask import request
import uuid

from datetime import datetime
from shutter_api.MySQL_command import *
from shutter_api.Responses import *


def publication(app) -> None:
    
    @app.route("/publications", methods=["GET"])
    def get_publications():
        
        try:
            tag = request.args.get('tag').strip()
        except ValueError:
            tag = []
            
        try:
            username = request.args.get('username').strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except ValueError:
            username = None
            
        try:
            page = int(request.args.get('page').strip())
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            page = 1
        except TypeError:
            return invalidParameter("page")
        
        
        if tag == []:
            data = getPublications(username=username, offset=page)
        else:
            data = getPublicationsFromTag(tag=tag,username=username,offset=page)
            
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
        
    
    @app.route("/publications", methods=["POST"])
    def post_publications():
        
        data = request.get_json()
        
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
            username = data["username"]
            if type(username) is not str:
                return invalidParameter("username")
            username = username.strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except KeyError:
            return missingParameterInJson("username")
        
        try:
            picture = data["picture"]
            if type(picture) is not str:
                return invalidParameter("picture")
            picture = picture.strip()
        except KeyError:
            return missingParameterInJson("picture")
        
        try:
            tags = data["tags"]
            if type(tags) != list:
                return invalidParameter("tags")  
        except KeyError:
            return missingParameterInJson("tags")

        for tag in tags:
            if type(tag) is not str:
                return invalidParameter("tags")
            tag = tag.strip()
            if not doesTagExist(tag):
                if not createTag(tag):
                    return invalidParameter(f"tag '{tag}'")
                
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
    def get_publication_publicationId(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter(publication_id)
        
        try:
            username = request.args.get('username').strip()
            if not doesUsernameExist(username):
                return invalidParameter("username")
        except ValueError:
            username = None
        
        data = getPublicationById(publication_id, username=username)
        if data is None:
            return requestFail()
        else:
            return ok(data=data)
    
    @app.route("/publications/<publication_id>/comments", methods=["POST"])
    def post_publications_publicationId_comments(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter(publication_id)
        
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
    def post_publication_publicationId_like(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter(publication_id)
        
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
            rating = data["rating"]
            if type(rating) is not bool:
                return invalidParameter("rating")
        except KeyError:
            return missingParameterInJson("rating")

        data = {
            "rating": str(int(rating)),
            "publication_id": publication_id,
            "username": username
        }
        
        if likePublication(data):
            return ok()
        else:
            return requestFail()

    
    @app.route("/publications/<publication_id>", methods=["DELETE"])
    def delete_publication_publicationId(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter(publication_id)
        
        if deletePublicationFromDB(publication_id):
            return deleteSucces()
        else:
            return deleteFail()
        
    @app.route("/publications/<publication_id>/comments", methods=["GET"])
    def get_publication_publicationId_comments(publication_id):
        
        if not doesPublicationExist(publication_id):
            return invalidParameter(publication_id)
        
        try:
            username = request.args.get('username').strip()
            if not doesUsernameExist(username):
                invalidParameter("username")
        except ValueError:
            username = None
            
        try:
            page = int(request.args.get('page'))
            if page < 1:
                return invalidParameter("page")
        except ValueError:
            page = 1
        except TypeError:
            return invalidParameter("page")
        
        data = getCommentsOfPublication(publication_id, username=username, offset=page)
        if data is None:
            return requestFail
        else:
            return ok(data=data)
            
    
    