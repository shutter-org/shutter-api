from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *
from shutter_api.MySQL_command.Publications import getCommentsOfPublication

def usernameFollowUser(follower:str, followed:str) -> bool:
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
    
def getFollowUser(username:str, offset:int=1) -> list or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT f.followed_username, u.profile_picture
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON u.username = f.followed_username
                       WHERE f.follower_username = "{username}"
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

def getFollowedUser(username:str, offset:int=1) -> list or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT f.follower_username, u.profile_picture
                       FROM {RELATION_TABLE_FOLLOW} f
                       LEFT JOIN {TABLE_USER} u ON u.username = f.follower_username
                       WHERE f.followed_username = "{username}"
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

def getuserFollowedPublication(username:str, offset:int = 1) -> list or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f'''
                        SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, SUM(IF(rp.rating = 0, -1, rp.rating)) AS sum_ratings, rp.rating AS user_rating 
                        FROM {TABLE_PUBLICATION} p 
                        JOIN {RELATION_TABLE_FOLLOW} f ON p.poster_username = f.followed_username
                        LEFT JOIN {RELATION_TABLE_RATE_PUBLICATION} rp ON p.publication_id = rp.publication_id
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        WHERE f.follower_username = "{username}"
                        ORDER BY p.created_date DESC
                        LIMIT 10
                        OFFSET {(offset-1) * 10};
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
                "rating": row[6] if row[6] is not None else 0,
                "user_rating": getIntFromRating(row[7]),
                "comments": getCommentsOfPublication(row[0],username=username)
            }
            data.append(post)
        
        return data
    except Exception:
        return None
