from shutter_api import MYSQL
from shutter_api.Tools import *
from shutter_api.MySQL_command.Publications import getCommentsOfPublication, getPublicationTags
from shutter_api.MySQL_command.Comments import getNumberOfCommentsFromPublication

def usernameFollowUser(follower:str, followed:str) -> bool:
    """
    add to db follower follow followed

    Args:
        follower (str): username of the follower
        followed (str): username of the folloed

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_FOLLOW} 
                       (follower_username, followed_username) 
                       VALUES ("{follower}","{followed}")
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def usernameUnfollowUser(follower:str, followed:str) -> bool:
    """
    remove from db follower follow followed

    Args:
        follower (str): username of the follower
        followed (str): username of the folloed

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_FOLLOW}
                       WHERE follower_username = "{follower}"
                       AND followed_username = "{followed}"
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def getFollowUserNumber(username:str) -> int or None:
    """
    get the number of user that follow the user

    Args:
        username (str): user username

    Returns:
        int or None: nb of follower, None if request Fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT COUNT(*)
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON BINARY u.username = f.followed_username
                       WHERE BINARY f.follower_username = "{username}"
                       ''')
        
        result = cursor.fetchall()[0][0]
        cursor.close()
        
        return result
    except Exception:
        return None

def getFollowUser(username:str, offset:int=1) -> list or None:
    """
    get the user that are being follow by username

    Args:
        username (str): user username
        offset (int, optional): foreach offset get the next 10 users. Defaults to 1.

    Returns:
        list or None: list of user, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT f.followed_username, u.profile_picture
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON BINARY u.username = f.followed_username
                       WHERE BINARY f.follower_username = "{username}"
                       LIMIT 50
                       OFFSET {(offset-1) * 50};
                       ''')
        
        result = cursor.fetchall()
        cursor.close()
        
        data = []
        for x in result:
            user = {
                "username":x[0],
                "profile_picture":x[1]
            }
            data.append(user)
        return data
    except Exception:
        return None

def getFollowedUserNumber(username:str) -> int or None:
    """
    get the number of user that are being follow by the user

    Args:
        username (str): user username

    Returns:
        int or None: nb of followed, None if request Fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT COUNT(*)
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON BINARY u.username = f.follower_username
                       WHERE BINARY f.followed_username = "{username}";
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return result
    except Exception:
        return None

def getFollowedUser(username:str, offset:int=1) -> list or None:
    """
    get the user that are being follow by username

    Args:
        username (str): user username
        offset (int, optional): foreach offset get the next 10 users. Defaults to 1.

    Returns:
        list or None: list of user, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT f.follower_username, u.profile_picture
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON BINARY u.username = f.follower_username
                       WHERE BINARY f.followed_username = "{username}"
                       LIMIT 50
                       OFFSET {(offset-1) * 50};
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        data = []
        for x in result:
            user = {
                "username":x[0],
                "profile_picture":x[1]
            }
            data.append(user)
        return data
    except Exception:
        return None
    
def getNbUserFollowedPublications(username:str) -> int or None:
    """
    Get the total nb of publication of the user that are being followed by username

    Args:
        username (str): user username

    Returns:
        int or None: nb of publicatons, None if request fail
    """
    
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f'''
                        SELECT COUNT(*)
                        FROM {TABLE_PUBLICATION} p 
                        JOIN {RELATION_TABLE_FOLLOW} f ON BINARY p.poster_username = f.followed_username
                        WHERE BINARY f.follower_username = "{username}";
                        ''')
        result = cursor.fetchall()[0][0]
        cursor.close()
        
        return result
    except Exception:
        return None

def getUserFollowedPublication(username:str, offset:int = 1) -> list or None:
    """
    get the most recent publications of the user being follow

    Args:
        username (str): user username
        offset (int, optional): foreach offset get the next 10 publications. Defaults to 1.

    Returns:
        list or None: list of publication, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f'''
                        SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, get_user_publication_rating("{username}",p.publication_id), p.rating
                        FROM {TABLE_PUBLICATION} p 
                        JOIN {RELATION_TABLE_FOLLOW} f ON BINARY p.poster_username = f.followed_username
                        LEFT JOIN {TABLE_USER} u ON BINARY p.poster_username = u.username
                        WHERE BINARY f.follower_username = "{username}"
                        ORDER BY p.created_date DESC
                        LIMIT 12
                        OFFSET {(offset-1) * 12};
                        ''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        
        for row in result:
            post = {
                "publication_id": row[0],
                "poster_user": {
                    "username":row[1],
                    "profile_picture":row[2]
                },
                "description": row[3],
                "picture": row[4],
                "created_date": getIntervalOdTimeSinceCreation(row[5]),
                "rating": row[7] if row[7] is not None else 0,
                "user_rating": getIntFromRating(row[6]),
                "comments": getCommentsOfPublication(row[0],username=username),
                "nb_comments": getNumberOfCommentsFromPublication(row[0]),
                "tags": getPublicationTags(row[0])
            }
            data.append(post)
        
        return data
    except Exception:
        return None
