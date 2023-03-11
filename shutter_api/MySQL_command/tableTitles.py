USER_TITLES = (
    "username",
    "password",
    "email",
    "name",
    "biography",
    "created_date",
    "birthdate",
    "profile_picture")

PUBLICATION_TITLES = (
    "publication_id",
    "poster_username",
    "description",
    "picture",
    "created_date"
)

GALLERY_TITLES = (
    "gallery_id",
    "creator_username",
    "description",
    "created_date",
    "private"
)

TAG_TITLES = (
    "value",
)

COMMENT_TITLES = (
    "comment_id",
    "commenter_username",
    "publication_id",
    "message",
    "created_date"
)

FOLLOW_TITLES = (
    "follower_username",
    "followed_username"
)

IDENTIFY_TITLES = (
    "publication_id",
    "tag_value"
)

RATE_GALLERY_TITLES = (
    "username",
    "gallery_id",
    "rating"
)

RATE_PUBLICATION_TITLES = (
    "username",
    "publication_id",
    "rating"
)

RATE_COMMENT_TITLES = (
    "username",
    "comment_id",
    "rating"
)