# Command
command pour run le serveur 
```
poetry run serve
```

# Router
| Type   | Path    |
| :---:  | :---   | 
| POST   | [/signup](#post-signup) |
| POST   | [/signin](#post-signin) |
| GET    | [/ping](#get-ping) |
|||
| GET    | [/users](#get-users)|
| GET    | [/users/«username»](#get-users«username») |
| PUT    | [/users/«username»](#put-users«username») |
| DELETE | [/users/«username»](#delete-users«username») |
| GET    | [/users/«username»/publications](#get-users«username»publications) |
| POST   | [/users/«username»/follow](#post-users«username»follow) |
| DELETE | [/users/«username»/follow](#delete-users«username»follow) |
| GET    | [/users/«username»/followers](#get-users«username»followers)|
| GET    | [/users/«username»/following](#get-users«username»following)|
| GET    | [/users/followed/publications](#get-users«username»followedpublication) |
|||
| GET    | [/comments/«comment_id»](#get-comments«comment_id») |
| PUT    | [/comments/«comment_id»](#put-comments«comment_id») |
| DELETE | [/comments/«comment_id»](#delete-comments«comment_id») |
| POST   | [/commments/«comment_id»/like](#post-comments«comment_id»like) |
| PUT    | [/commments/«comment_id»/like](#put-comments«comment_id»like) |
| DELETE | [/commments/«comment_id»/like](#delete-comments«comment_id»like) |
|||
| POST   | [/gallerys](#post-gallerys) |
| GET    | [/gallerys/«gallery_id»](#get-gallerys«gallery_id») |
| PUT    | [/gallerys/«gallery_id»](#put-gallerys«gallery_id») |
| DELETE | [/gallerys/«gallery_id»](#delete-gallerys«gallery_id») |
| GET    | [/gallerys/«gallery_id»/publications](#get-gallerys«gallery_id»publications) |
| POST   | [/gallerys/«gallery_id»/publications](#post-gallerys«gallery_id»publications) |
| DELETE | [/gallerys/«gallery_id»/publications](#delete-gallerys«gallery_id»publications) |
| POST   | [/gallerys/«gallery_id»/like](#post-gallerys«gallery_id»like) |
| PUT    | [/gallerys/«gallery_id»/like](#put-gallerys«gallery_id»like) |
| DELETE | [/gallerys/«gallery_id»/like](#delete-gallerys«gallery_id»like) |
|||
| GET    | [/publications](#get-publications) |
| POST   | [/publications](#post-publications) |
| GET    | [/publications/«publication_id»](#get-publications«publication_id») |
| PUT    | [/publications/«publication_id»](#put-publications«publication_id») |
| DELETE | [/publications/«publication_id»](#delete-publications«publication_id») |
| GET    | [/publications/«publication_id»/comments](#get-publications«publication_id»comments) |
| POST   | [/publications/«publication_id»/comments](#post-publications«publication_id»comments) |
| POST   | [/publications/«publication_id»/like](#post-publications«publication_id»like) |
| PUT    | [/publications/«publication_id»/like](#put-publications«publication_id»like) |
| DELETE | [/publications/«publication_id»/like](#delete-publications«publication_id»like) |
|||
| GET    | [/tags](#get-tags) |



---

### POST /signup
This route is used to create a new user.

input body:
```
{
    "username" : String,
    "password" : String,
    "email" : String,
    "name" : String,
    "birthdate": String (yyyy/mm/dd)
}
```
output body, code 201:
```
{
    "msg" : "creation succes"
}
```
---
### POST /signIn
This route is used to obtain an access token. 

input body: 
```
{
    "username" : String,
    "password" : String
}
```
output body connection succes, code 200
```
{
    "access_token" : String,
    "user":{
        "username": String,
        "profile_picture": String (image URL) 
    }

}
```
output body connection fail, code 401
```
{
    "Error": "connection failure"
}
```
---
### GET /ping
**Access_token needed**.

Check if the access token is still valid.

output body, code 200:
```
{
    "msg": "ok"
}
```

---
### GET /users
**Access_token needed**.

This route allows you to search for users using the 'search' parameter. By default, the route returns 12 users at a time. You can request additional users by specifying the 'page' parameter. If no search parameter is present, the route will search for all users. If no page parameter is specified, the first page is returned by default.

Please note that the list of followers and following is limited to 50. If you require more, you can make additional requests to [GET /users/«username»/followers](#get-users«username»followers) and [GET /users/«username»/following](#get-users«username»following)


exemple :
```
api/users?search=...&page=int>0
```
output body, code 200:
```
[
    {
        "name": String,
        "profile_picture": String (URL),
        "username": String
    },
    ...
]
```
---
### GET /users/«username»
**Access_token needed**.

This route provides all information about a user. If a user is viewing their own page, more information will be included in the output. The lists of followers and following are limited to 50 users each. If you require more, you can make additional requests using the following routes: [GET /users/«username»/followers](#get-users«username»followers) or [GET /users/«username»/following](#get-users«username»following).

The number of publications shown is limited to 12. If you require more, you can make additional requests using [GET /users/«username»/publications]((#get-users«username»publications)).Similarly, the number of publications in a gallery is also limited to 12. If you require more, you can make additional requests using [GET /gallerys/«gallery_id»/publications](#get-gallerys«gallery_id»publications).

Note that if the username does not match the access token, private galleries will not be shown.

output body if username doesn't match access_token, 200:
```
{
    "age": int,
    "biography": String,
    "created_date": Sting,
    "followed_by_user": Boolean,
    "followers":[
        {
            "profile_picture": String (URL),
            "username": String
        },
        ...
    ],
    "following":[
        {
            "profile_picture": String (URL),
            "username": String
        },
        ...
    ],
    "gallerys":[
        {
            "gallery_id": String
            "publications": [
                {
                    "picture": String (URL),
                    "publication_id": String
                },
                ...
            ],
            "title": String
        },
        ...
    ],
    "name": String,
    "nb_followes": int,
    "nb_following": int,
    "nb_publications": int,
    "profile_picture": String (URL),
    "publications" : [
        {
            "created_date": String,
            "picture": String (URL),
            "publication_id"
        },
        ...
    ],
    "username": String
}
```

output body if username belong to access_token, code 200:
```
{
    "age": int,
    "biography": String,
    "birthdate": String,
    "created_date": Sting,
    "email": String,
    "followers":[
        {
            "profile_picture": String (URL),
            "username": String
        },
        ...
    ],
    "following":[
        {
            "profile_picture": String (URL),
            "username": String
        },
        ...
    ],
    "gallerys":[
        {
            "gallery_id": String
            "publications": [
                {
                    "picture": String (URL),
                    "publication_id": String
                },
                ...
            ],
            "title": String
        },
        ...
    ],
    "name": String,
    "nb_followes": int,
    "nb_following": int,
    "nb_publications": int,
    "profile_picture": String (URL),
    "publications" : [
        {
            "created_date": String,
            "picture": String (URL),
            "publication_id"
        },
        ...
    ],
    "username": String
}
```
---
### PUT /users/«username»
**Access_token needed**.

This route allows modification of a user's data. Access is only granted to the user whose username matches the access token.

You can modify one or more parameters at a time. Simply send the field that needs to be updated.

input body: 
```
{
    "biography": String,
    "email": String,
    "password": String,
    "username": String,
    "name": String,
    "profile_picture": image base64 or String (URL)
}
```

output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /users/«username»
**Access_token needed**.

Access to this route is granted only to the user whose username matches the access token. This route is used to delete all data related to the user, including the user account itself.

output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /users/«username»/publications
**Access_token needed**.

This route returns the publications of the specified username. By default, the route returns up to 12 publications per page. To obtain additional publications, you can change the 'page' parameter to request the next batch of results. If the 'page' parameter is not specified, the first page of results is returned.

exemple :
```
api/users?page=int>0
```

output body, code 200:
```
[
    {
        "created_date": String,
        "picture": String (URL),
        "publication_id": String
    },
    ...
]
```
---
### POST /users/«username»/follow
**Access_token needed**.

This route is used to follow a user.

output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /users/«username»/follow
**Access_token needed**.

This route is used to unfollow a user.

output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /users/«username»/followers
**Access_token needed**.

This route returns a list of users who are following the specified user. By default, the list is limited to 50 users per page. To obtain additional results, you can change the 'page' parameter to request the corresponding page. If the 'page' parameter is not specified, the first page of results is returned.

exemple :
```
api/users/«username»/followers?page=int>0
```

output body, code 200:
```
[
    {
        "profile_picture": String (URL),
        "username": String
    },
    ...
]
```
---
### GET /users/«username»/following
**Access_token needed**.

This route returns a list of users who are being followed by the specified user. By default, the list is limited to 50 users per page. To obtain additional results, you can change the 'page' parameter to request the corresponding page. If the 'page' parameter is not specified, the first page of results is returned.

exemple :
```
api/users/«username»/following?page=int>0
```

output body, code 200:
```
[
    {
        "profile_picture": String (URL),
        "username": String
    },
    ...
]
```
---
### GET /users/followed/publications
**Access_token needed**.

This route returns an object containing the total number of publications and a list of up to 12 publications. To obtain the next batch of publications, you can change the 'page' parameter. The number of comments for each publication is also limited, but you can obtain additional comments by calling the [GET /publications/«publication_id»/comments](#get-publications«publication_id»comments)

exemple :
```
api/users/followed/publications?page=int>0
```

output body, code 200:
```
{
    "nb_publications":int
    "publication":[
        {
            "comments": [
                {
                    "comment_id" : String,
                    "commenter_user":{
                        "profile_picture": String (URL),
                        "username": String
                    }
                    "created_date": String,
                    "message": String,
                    "rating" : int,
                    "user_rating": int
                },
                ...
            ],
            "created_date": String,
            "description": String,
            "nb_comments": Int,
            "picture": String (URL),
            "poster_user":{
                "profile_picture": String(URL),
                "username": String
            }
            "publication_id": String,
            "rating": int,
            "tags": [String],
            "user_rating": int
        },
        ...
    ]
}
```
---
### GET /comments/«comment_id»
**Access_token needed**.

This route is used to retrieve data for a specific comment.

Output body, code 200:
```
{
    "comment_id": String,
    "commenter_username": String,
    "message": String,
    "created_date": String,
    "publication_id": String,
    "rating": int
}
```
---
### PUT /comments/«comment_id»
**Access_token needed**.

This route is used to change the message of a comment. Only the creator of the comment can access this route.

Input body:
```
{
    "message":String
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /comments/«comment_id»
**Accesss_token needed**.

This route is used to delete a comment. Only the creator of the comment or the creator of the publication to which the comment belongs can access this route.

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### POST /comments/«comment_id»/like
**Access_token needed**.

The purpose of this feature is to enable users to rate comments. Each user is limited to rating a comment only once.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### PUT /comments/«comment_id»/like
**Access_token needed**.

This route allows users to update their rating of a comment they have previously rated.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /comments/«comment_id»/like
**Access_token needed**.

The purpose of this route is to enable users to remove their rating on a comment.


Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### POST /gallerys
**Access_token needed**.

The purpose of this route is to allow users to create a new gallery, which they can use to store and organize their images or other multimedia content.

Input body:
```
{
    "description": String,
    "title": String,
    "private": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /gallerys/«gallery_id»
**Access_token needed**.

"The purpose of this route is to retrieve the data of a gallery. When retrieving the list of publications associated with the gallery, only the first 12 publications are included. To retrieve additional publications, the user must make a subsequent request using the [GET /gallerys/«gallery_id»/publications](#get-gallerys«gallery_id»publications)



Output body, code 200:
```
{
    "created_date": String,
    "creator_user": {
        "profile_picture": String (URL),
        "username": String
    },
    "description": String,
    "gallery_id": String,
    "nb_publicaitons": int,
    "publications":[
        {
            "picture": String (URL),
            "publications_id": String
        },
        ...
    ],
    "rating": int,
    "tile": String,
    "user_rating" : int
}
```
---
### PUT /gallerys/«gallery_id»
**Access_token needed**.

The purpose of this route is to allow the creator of a gallery to modify it. Only the creator of the gallery has access to this route. The user can include one or more fields in the request body to specify the changes they want to make.

Input body:
```
{
    "description": String,
    "title": String,
    "private": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /gallerys/«gallery_id»
**Access_token needed**.

The purpose of this route is to enable the creator of a gallery to delete it. Only the user who created the gallery has access to this route, and once the gallery is deleted, it cannot be restored.

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /gallerys/«gallery_id»/publications
**Access_token needed**.

The purpose of this route is to retrieve a list of publications associated with a gallery. The list is limited to 12 publications per page. To retrieve the next batch of publications, the user can change the page parameter accordingly. If the page parameter is not present, the endpoint returns the first page by default.

exemple:
```
GET /gallerys/«gallery_id»/publications?page=int>0
```

Output body, code 200:
```
[
    {
        "picture": String (URL),
        "publications_id": String
    },
    ...
],
```
---
### POST /gallerys/«gallery_id»/publications
**Access_token needed**.

The purpose of this route is to allow the creator of a gallery to add a publication to it. Only the user who created the gallery has access to this route, and the added publication will be associated with the gallery.

Input body:
```
{
    "publication_id": String
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /gallerys/«gallery_id»/publications
**Access_token needed**.

The purpose of this route is to enable the creator of a gallery to remove a publication from it. Only the user who created the gallery has access to this route, and the publication will be disassociated from the gallery.

Input body:
```
{
    "publication_id": String
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### POST /gallerys/«gallery_id»/like
**Access_token needed**.

The purpose of this route is to allow users to rate a gallery. Each user can only rate a gallery once.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```

---
### PUT /gallerys/«gallery_id»/like
**Access_token needed**.

The purpose of this route is to enable users to update their rating of a gallery that they have previously rated.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /gallerys/«gallery_id»/like
**Access_token needed**.

The purpose of this route is to allow users to remove their rating of a gallery.


Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /publications
**Access_token needed**.

The purpose of this route is to retrieve the most recent publications. The list is limited to 12 publications per page, and the user can retrieve the next batch of publications by including the page parameter. To retrieve publications related to a specific tag, the user can include the tag parameter. The same applies to retrieving comments for a publication, where the user can use the [GET /publications/«publication_id»/comments](#get-publications«publication_id»comments) endpoint to retrieve additional comments. 

exemple:
```
GET /publications?page=int>0&tag=...
```


Output body, code 200:
```
{
    "nb_publications": int,
    "publications":[
        {
            "comments":[
                {
                    "comment_id": String,
                    "commenter_user":{
                        "profile_picture": String (URL),
                        "username": String
                    },
                    "created_date": Sting,
                    "message": String,
                    "rating": int,
                    "user_rating": int
                },
                ...
            ]
            "created_date": String,
            "description": String,
            "nb_comments": int,
            "picture": String (URL),
            "poster_user":{
                "profile_picture": String (URL),
                "username": String
            },
            "publication_id": String,
            "rating": int,
            "tags": [String],
            "user_rating": int
        },
        ...
    ]
}
```
---
### POST /publications
**Access_token needed**.

The purpose of this route is to enable users to create a new publication, which will be added to the list of existing publications.

Input body:
```
{
    "description": String,
    "picture": String (URL),
    "tags": [String]
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /publications/«publication_id»
**Access_token needed**.

"The purpose of this route is to retrieve data for a specific publication, including its content and associated metadata. The list of comments associated with the publication is limited to 12 comments per page, and the user can retrieve additional comments by using the  [GET /publications/«publication_id»/comments](#get-publications«publication_id»comments)



Output body, code 200:
```
{
    "comments":[
        {
            "comment_id": String,
            "commenter_user":{
                "profile_picture": String (URL),
                "username": String
            },
            "created_date": Sting,
            "message": String,
            "rating": int,
            "user_rating": int
        },
        ...
    ]
    "created_date": String,
    "description": String,
    "nb_comments": int,
    "picture": String (URL),
    "poster_user":{
        "profile_picture": String (URL),
        "username": String
    },
    "publication_id": String,
    "rating": int,
    "tags": [String],
    "user_rating": int
}
```
---
### PUT /publications/«publication_id»
**Access_token needed**.

The purpose of this route is to allow the creator of a publication to modify its content and associated metadata. Only the user who created the publication has access to this route, and the user can specify one or more fields to modify in the request body.

Input body:
```
{
    "tags": [String],
    "description": String
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /publications/«publication_id»
**Access_token needed**.

The purpose of this route is to allow the creator of a publication to delete it. Only the user who created the publication has access to this route.

Output body, code 200:
```
{
    "msg": "ok"
}
```

---
### GET /publications/«publication_id»/comments
**Access_token needed**.

The purpose of this route is to retrieve a list of comments associated with a publication. The list is limited to 12 comments per page, and the user can retrieve the next batch of comments by including the page parameter. If the page parameter is not present, the first page of comments will be returned by default.

exemple:
```
GET /publications/«publication_id»/comments?page=int>0
```

Output body, code 200:
```
[
    {
        "comment_id": String,
        "commenter_user":{
            "profile_picture": String (URL),
            "username": String
        },
        "created_date": Sting,
        "message": String,
        "rating": int,
        "user_rating": int
    },
    ...
]
```
---
### POST /publications/«publication_id»/comments
**Access_token needed**.

The purpose of this route is to allow users to create a new comment for a specific publication. Once the comment is created, it will be added to the list of comments associated with the publication.

Input body:
```
{
    "message": String
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### POST /publications/«publication_id»/like
**Access_token needed**.

The purpose of this route is to allow users to add a rating to a publication. Each user can only rate a publication once.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### PUT /publications/«publication_id»/like
**Access_token needed**.

The purpose of this route is to allow a user to update their rating on a specific publication.

Input body:
```
{
    "rating": Boolean
}
```

Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### DELETE /publications/«publication_id»/like
**Access_token needed**.

The purpose of this route is to allow a user to remove their rating from a specific publication.


Output body, code 200:
```
{
    "msg": "ok"
}
```
---
### GET /tags
**Access_token needed**.

The purpose of this route is to provide a search function that returns a list of tags based on the user's search parameter.

exemple:
```
GET /tags?search=...
```


Output body, code 200:
```
[
    {
        "nb_publications": int
        "tag": String
    },
    ...
]
```
---
