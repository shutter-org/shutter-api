# Command
command pour run le serveur 
```
poetry run serve
```

# Router
| Type   | Path    |
| :---:  | :---   | 
| POST   | [/signup](#postsignup) |
| POST   | [/signin](#postsignin) |
|||
| GET    | [/users](#getusers)|
| GET    | [/users/«username»](#getusers«username») |
| PUT    | [/users/«username»](#putusers«username») |
| DELETE | [/users/«username»](#deleteusers«username») |
| GET    | [/users/«username»/details](#getusers«username»details) |
| POST   | [/users/«username»/follow](#postusers«username»follow) |
| DELETE | [/users/«username»/follow](#deleteusers«username»follow) |
| GET    | [/users/«username»/followers]()|
| GET    | [/users/«username»/following]()|
| GET    | [/users/followed/publications](#getusers«username»followedpublication) |
|||
| GET    | /comments/«comment_id» |
| DELETE | /comments/«comment_id» |
| PUT    | /comments/«comment_id» |
| POST   | /commments/«comment_id»/like |
| PUT    | /commments/«comment_id»/like |
| DELETE | /commments/«comment_id»/like |
|||
| POST   | /gallerys |
| GET    | /gallerys/«gallery_id» |
| PUT    | /gallerys/«gallery_id» |
| DELETE | /gallerys/«gallery_id» |
| GET    | /gallerys/«gallery_id»/publications |
| POST   | /gallerys/«gallery_id»/publications |
| DELETE | /gallerys/«gallery_id»/publications |
| POST   | /gallerys/«gallery_id»/like |
| PUT    | /gallerys/«gallery_id»/like |
| DELETE | /gallerys/«gallery_id»/like |
|||
| GET    | /publications |
| POST   | /publications |
| GET    | /publications/«publication_id» |
| PUT    | /publications/«publication_id» |
| DELETE | /publications/«publication_id» |
| GET    | /publications/«publication_id»/comments |
| POST   | /publications/«publication_id»/comments |
| POST   | /publications/«publication_id»/like |
| PUT    | /publications/«publication_id»/like |
| DELETE | /publications/«publication_id»/like |
|||
| GET    | /ping |

---

### POST/signup
This route is to create a new user

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
output body, code 200:
```
{
    "msg" : "creation succes"
}
```
---
### POST/signIn
This route is to get an acces token 

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
    "acces_token" : String,
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
### GET/users
**Acces_token needed**.
This route is to get the users with the help of the search param. This route will give you 10 users at a time if you want more publicaiton you can call the page param to get more. If the search param is not present search from all users. if page parame is not present base value of 1.

The list of follower and following are limited to 50, if you want more you can call 


example :
```
api/users?search=...&page=int>1
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
### GET/users/«username»
**Acces_token needed**.
This route is to get all the info about a user. if the user is checking his page there is more information in the output. for the followers and following, it is limited to 50 users each, if you want more call this route [get /users/u]()

output body if username belong to acces_token, code 200:
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
### PUT/users/«username»

---
### DELETE/users/«username»
---
### GET/users/«username»/details
---
### POST/users/«username»/follow
---
### DELETE/users/«username»/follow
---
---
### GET/users/«username»/followed/publication
---
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