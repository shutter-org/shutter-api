from shutter_api import MYSQL
from .publication import getCommentsOfPublication
from .gallery import getGalleryPublications
from datetime import datetime, date
from .tableName import *
from .tableTitles import *

def doesUsernameExist(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT username FROM {TABLE_USER} WHERE username = "{userName}"; ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT email FROM {TABLE_USER} WHERE email = "{email}"; ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 0
    except Exception:
        return False
    
def doesUserFollowUsername(follower:str, followed) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_FOLLOW} 
                       WHERE follower_username = "{follower}"
                       AND followed_username = "{followed}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False

def updateUser(username:str, newUsername:str=None, email:str=None, bio:str=None, picture:str=None) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       UPDATE {TABLE_USER} u 
                       SET 
                       {f"""u.username = "{newUsername}" """ if newUsername is not None else ""}
                       {f"""{"," if newUsername is not None else ""}u.email = "{email}" """ if email is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None else ""}u.biography = "{bio}" """ if bio is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None else ""}u.profile_picture = "{picture}" """ if picture is not None else ""}
                       WHERE u.username = "{username}"; ''')
        conn.commit()
        
        cursor.close()
        return True
    except ValueError:
        return False

def deleteUserFromDB(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_USER} 
                       WHERE username = "{userName}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except ValueError:
        return False
    
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
    
def getUserGallery(username:str, private:bool) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id, g.title
                       FROM {TABLE_GALLERY} g
                       WHERE g.creator_username = "{username}" {f""" AND g.private = false""" if not private else ""}
                       ORDER BY g.created_date DESC
                       ''')
        result = cursor.fetchall()
        cursor.close()
        gallerys = []
        for x in result:
            data = {
                "gallery_id": x[0],
                "title":x[1],
                "publications":getGalleryPublications(x[0], username=username)
            }
            gallerys.append(data)
        
        
        return gallerys
    except Exception:
        return None
    
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
    
def getuserFollowedPublication(username:str, offset:int = 1) -> list:
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
                        GROUP BY p.publication_id
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
                "created_date": row[5].strftime('%Y-%m-%d %H:%M:%S'),
                "rating": row[6] if row[6] is not None else 0,
                "user_rating":0 if row[7] is None else (1 if row[7] == b'\x01' else -1),
                "comments": getCommentsOfPublication(row[0],username=username)
            }
            data.append(post)
        
        return data
    except Exception:
        return None


def getUserByUsername(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT u.username, u.biography, u.name, u.birthdate, u.profile_picture FROM {TABLE_USER} u WHERE username = "{username}" ''')
        result = cursor.fetchall()[0]
        
        cursor.close()
        today = date.today()
        age = today.year - result[3].year - ((today.month, today.day) < (result[3].month, result[3].day))
        data = {
            "username": result[0],
            "biography":result[1],
            "name":result[2],
            "age":age,
            "profile_picture":result[4]
        }
    
        return data
    except ValueError:
        return None
    
def getUserByUsernameDetail(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT u.username, u.email, u.biography, u.name, u.created_date, u.birthdate, u.profile_picture FROM {TABLE_USER} u WHERE username = "{username}" ''')
        result = cursor.fetchall()[0]
        
        cursor.close()
        today = date.today()
        age = today.year - result[5].year - ((today.month, today.day) < (result[5].month, result[5].day))
        data = {
            "username": result[0],
            "email":result[1],
            "biography":result[2],
            "name":result[3],
            "created_date": result[4].strftime('%Y-%m-%d'),
            "birthdate":result[5].strftime('%Y-%m-%d'),
            "age":age,
            "profile_picture":result[6]
        }
    
        return data
    except Exception:
        return None
    
