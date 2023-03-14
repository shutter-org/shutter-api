CREATE DATABASE shutter;

USE shutter;

/* entity */
CREATE TABLE user(username VARCHAR(50) NOT NULL, password VARCHAR(50), email VARCHAR(50),
 name VARCHAR(50), biography VARCHAR(100), created_date DATETIME, birthdate DATE,
  profile_picture VARCHAR(2000), PRIMARY KEY(username));

CREATE TABLE publication(publication_id VARCHAR(36) NOT NULL, poster_username VARCHAR(50) NOT NULL,
 description VARCHAR(200), picture VARCHAR(2000), created_date DATETIME,
  PRIMARY KEY (publication_id), FOREIGN KEY(poster_username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE gallery(gallery_id VARCHAR(36) NOT NULL, creator_username VARCHAR(50) NOT NULL,
 description VARCHAR(200), created_date DATETIME, private BIT(1),
  PRIMARY KEY(gallery_id), FOREIGN KEY(creator_username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE tag(value VARCHAR(50) NOT NULL, PRIMARY KEY(value));

CREATE TABLE comment(comment_id VARCHAR(36) NOT NULL,
 commenter_username VARCHAR(50) NOT NULL, publication_id VARCHAR(36) NOT NULL,
  message VARCHAR(200), created_date DATETIME,
   PRIMARY KEY(comment_id), FOREIGN KEY(commenter_username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(publication_id) REFERENCES publication(publication_id) ON DELETE CASCADE ON UPDATE CASCADE);


/* Relationship */
CREATE TABLE follow(follower_username VARCHAR(36) NOT NULL, followed_username VARCHAR(36) NOT NULL,
 PRIMARY KEY(follower_username, followed_username),
  FOREIGN KEY(follower_username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(followed_username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE identify(publication_id VARCHAR(36) NOT NULL, tag_value VARCHAR(50) NOT NULL,
 PRIMARY KEY(publication_id, tag_value),
  FOREIGN KEY(publication_id) REFERENCES publication(publication_id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(tag_value) REFERENCES tag(value));

CREATE TABLE save(gallery_id VARCHAR(36) NOT NULL, publication_id VARCHAR(36) NOT NULL,
 PRIMARY KEY(gallery_id, publication_id),
  FOREIGN KEY(gallery_id) REFERENCES gallery(gallery_id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(publication_id) REFERENCES publication(publication_id) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE rate_gallery(username VARCHAR(50) NOT NULL, gallery_id VARCHAR(36) NOT NULL, rating BIT(1),
 PRIMARY KEY(username, gallery_id),
  FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(gallery_id) REFERENCES gallery(gallery_id) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE rate_publication(username VARCHAR(50) NOT NULL, publication_id VARCHAR(36) NOT NULL, rating BIT(1),
 PRIMARY KEY (username, publication_id),
  FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(publication_id) REFERENCES publication(publication_id) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE rate_comment(username VARCHAR(50) NOT NULL, comment_id VARCHAR(36) NOT NULL, rating BIT(1),
 PRIMARY KEY (username, comment_id),
  FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY(comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE ON UPDATE CASCADE);
