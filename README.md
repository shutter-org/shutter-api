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
| GET    | [/users/«username»/details](#getusers«username»details) |
| POST   | [/users/«username»/follow](#postusers«username»follow) |
| GET    | [/users/«username»/followed/publications](#getusers«username»followedpublication) |
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
---
### POST/signIn
---
### GET/users/«username»
---
### DELETE/users/«username»
---
### GET/users/«username»/details
---
### POST/users/«username»/follow
---
### GET/users/«username»/followed/publication
---