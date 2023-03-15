from shutter_api import MYSQL
from .publication import getCommentsOfPublication
from datetime import datetime, date
from .tableName import *
from .tableTitles import *

def doesUsernameExist(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT username FROM {TABLE_USER} WHERE username = "{userName}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT email FROM {TABLE_USER} WHERE email = "{email}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 0
    except Exception:
        return False

def deleteUserFromDB(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_USER} WHERE username = "{userName}" ''')
        conn.commit()
        
        cursor.close()
        return True
    except ValueError:
        return False
    
def usernameFollowUser(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_FOLLOW} (follower_username, followed_username) VALUES (
            "{data["follower_username"]}",
            "{data["followed_username"]}")''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def getFollowUser(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT followed_username FROM {RELATION_TABLE_FOLLOW} WHERE follower_username = "{username}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
    except Exception:
        return None
    
def getUserGallery(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id 
                       FROM {TABLE_GALLERY} g
                       WHERE g.creator_username = "{username}"
                       ORDER BY g.created_date DESC
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
    except Exception:
        return None

def getFollowedUser(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT follower_username FROM {RELATION_TABLE_FOLLOW} WHERE followed_username = "{username}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
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
                "comment": getCommentsOfPublication(row[0],username=username)
            }
            data.append(post)
        
        return data
    except ValueError:
        return None


def getUserByUsernname(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT u.username, u.email, u.biography, u.name, u.created_date, u.birthdate, u.profile_picture FROM {TABLE_USER} u WHERE username = "{username}" ''')
        result = cursor.fetchall()[0]
        
        cursor.close()
        
        data = {
            "username": result[0],
            "email":result[1],
            "biogreaphy":result[2],
            "name":result[3],
            "created_date": result[4].strftime('%Y-%m-%d %H:%M:%S'),
            "birthdate":result[5].strftime('%Y-%m-%d'),
            "profile_picture":result[6]
        }
    
        return data
    except Exception as e:
        return None
    
def getAllUser() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {TABLE_USER} ''')
    result = cursor.fetchall()
    print(result)
    cursor.close()
    
def getALLFollow() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_FOLLOW} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
