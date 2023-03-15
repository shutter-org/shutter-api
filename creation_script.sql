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

/* Function */

DELIMITER //
CREATE FUNCTION get_user_comment_rating(
    p_username VARCHAR(50),
    p_comment_id VARCHAR(36)
)
RETURNS BIT(1)
BEGIN
    DECLARE v_rating INT;
    SELECT rating INTO v_rating
    FROM rate_comment
    WHERE username = p_username AND comment_id = p_comment_id;
    RETURN v_rating;
END//
DELIMITER ;

DELIMITER //
CREATE FUNCTION get_user_publication_rating(
    p_username VARCHAR(50),
    p_publication_id VARCHAR(36)
)
RETURNS BIT(1)
BEGIN
    DECLARE v_rating INT;
    SELECT rating INTO v_rating
    FROM rate_publication
    WHERE username = p_username AND publication_id = p_publication_id;
    RETURN v_rating;
END//
DELIMITER ;

DELIMITER //
CREATE FUNCTION get_user_gallery_rating(
    p_username VARCHAR(50),
    p_gallery_id VARCHAR(36)
)
RETURNS BIT(1)
BEGIN
    DECLARE v_rating INT;
    SELECT rating INTO v_rating
    FROM rate_gallery
    WHERE username = p_username AND gallery_id = p_gallery_id;
    RETURN v_rating;
END//
DELIMITER ;

/* Procedure */
DELIMITER //
CREATE PROCEDURE update_comment_rating_procedure(IN comment_id_var VARCHAR(36))
BEGIN
    DECLARE total_rating INT;
    SET total_rating = (
        SELECT SUM(CASE WHEN rc.rating = 1 THEN 1 WHEN rc.rating = 0 THEN -1 ELSE 0 END)
        FROM rate_comment rc
        WHERE comment_id_var = rc.comment_id
    );
    UPDATE comment
    SET rating = total_rating
    WHERE comment_id_var = comment_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_publication_rating_procedure(IN publication_id_var VARCHAR(36))
BEGIN
    DECLARE total_rating INT;
    SET total_rating = (
        SELECT SUM(CASE WHEN rp.rating = 1 THEN 1 WHEN rp.rating = 0 THEN -1 ELSE 0 END)
        FROM rate_publication rp
        WHERE publication_id_var = rp.publication_id
    );
    UPDATE publication p
    SET p.rating = total_rating
    WHERE publication_id_var = p.publication_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_gallery_rating_procedure(IN gallery_id_var VARCHAR(36))
BEGIN
    DECLARE total_rating INT;
    SET total_rating = (
        SELECT SUM(CASE WHEN rg.rating = 1 THEN 1 WHEN rg.rating = 0 THEN -1 ELSE 0 END)
        FROM rate_gallery rg
        WHERE gallery_id_var = rg.gallery_id
    );
    UPDATE gallery g
    SET g.rating = total_rating
    WHERE gallery_id_var = g.gallery_id;
END//
DELIMITER ;

/* rate_comment Trigger */
DELIMITER //
CREATE TRIGGER update_comment_rating_insert
AFTER INSERT ON rate_comment
FOR EACH ROW
BEGIN
    CALL update_comment_rating_procedure(NEW.comment_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_comment_rating_update
AFTER UPDATE ON rate_comment
FOR EACH ROW
BEGIN
    CALL update_comment_rating_procedure(NEW.comment_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_comment_rating_delete
AFTER DELETE ON rate_comment
FOR EACH ROW
BEGIN
    CALL update_comment_rating_procedure(OLD.comment_id);
END//
DELIMITER ;

/* rate_publication trigger*/
DELIMITER //
CREATE TRIGGER update_publication_rating_insert
AFTER INSERT ON rate_publication
FOR EACH ROW
BEGIN
    CALL update_publication_rating_procedure(NEW.publication_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_publication_rating_update
AFTER UPDATE ON rate_publication
FOR EACH ROW
BEGIN
    CALL update_publication_rating_procedure(NEW.publication_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_publication_rating_delete
AFTER DELETE ON rate_publication
FOR EACH ROW
BEGIN
    CALL update_publication_rating_procedure(OLD.publication_id);
END//
DELIMITER ;

/* rate_galery trigger*/
DELIMITER //
CREATE TRIGGER update_gallery_rating_insert
AFTER INSERT ON rate_gallery
FOR EACH ROW
BEGIN
    CALL update_gallery_rating_procedure(NEW.gallery_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_gallery_rating_update
AFTER UPDATE ON rate_gallery
FOR EACH ROW
BEGIN
    CALL update_gallery_rating_procedure(NEW.gallery_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_gallery_rating_delete
AFTER DELETE ON rate_gallery
FOR EACH ROW
BEGIN
    CALL update_gallery_rating_procedure(OLD.gallery_id);
END//
DELIMITER ;