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
| GET    | [/users/«username»](#getusers«username») |
| DELETE | [/users/«username»](#deleteusers«username») |
| POST   | [/users/«username»/follow](#postusers«username»follow) |
| GET    | [/users/«username»/followed/publications](#getusers«username»followedpublication) |
|||
| GET    | /comments/«comment_id» |
| DELETE | /comments/«comment_id» |
| POST   | /commments/«comment_id»/like |
|||
| POST   | /gallerys |
| GET    | /gallerys/«gallery_id» |
| POST   | /gallerys/«gallery_id» |
| DELETE | /gallerys/«gallery_id» |
| GET    | /gallerys/«gallery_id»/publications |
| POST   | /gallerys/«gallery_id»/like |
|||
| GET    | /publications |
| POST   | /publications |
| GET    | /publications/«publication_id» |
| DELETE | /publications/«publication_id» |
| GET   | /publications/«publication_id»/comments |
| POST  | /publications/«publication_id»/comments |
| POST  | /publications/«publication_id»/like |

---

### POST/signup
input body
```
{
    "username" : String,
    "password" : String,
    "email" : String,
    "name" : String,
    "birthdate": String (yyyy/mm/dd)
}
```
output body
```
{
    "username": String
}
```
---
### POST/signIn
---
### GET/users/«username»
---
### DELETE/users/«username»
---
### POST/users/«username»/follow
---
### GET/users/«username»/followed/publication
---