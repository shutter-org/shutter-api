TITLES_USER = (
    "username",
    "password",
    "email",
    "name",
    "biography",
    "created_date",
    "birthdate",
    "profile_picture")

TITLES_PUBLICATION = (
    "publication_id",
    "poster_username",
    "description",
    "picture",
    "created_date"
)

TITLES_GALLERY = (
    "gallery_id",
    "creator_username",
    "description",
    "created_date",
    "private"
)

TITLES_TAG = (
    "value",
)

TITLE_SAVE = (
    "gallery_id",
    "publication_id"
)

TITLES_COMMENT = (
    "comment_id",
    "commenter_username",
    "publication_id",
    "message",
    "created_date"
)

TITLES_FOLLOW = (
    "follower_username",
    "followed_username"
)

TITLES_IDENTIFY = (
    "publication_id",
    "tag_value"
)

TITLES_RATE_GALLERY = (
    "username",
    "gallery_id",
    "rating"
)

TITLES_RATE_PUBLICATION = (
    "username",
    "publication_id",
    "rating"
)

TITLES_RATE_COMMENT = (
    "username",
    "comment_id",
    "rating"
)