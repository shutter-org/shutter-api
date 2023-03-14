from shutter_api import MYSQL
import struct
from datetime import datetime, date
from .tableName import *
from .tableTitles import *

def doesUsernameExist(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT username FROM {TABLE_USER} WHERE username = '{userName}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT email FROM {TABLE_USER} WHERE email = '{email}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 0
    except Exception:
        return False

def deleteUserFromDB(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_USER} WHERE username = '{userName}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def usernameFollowUser(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_FOLLOW} (follower_username, followed_username) VALUES (
            '{data["follower_username"]}',
            '{data["followed_username"]}')''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def getFollowUser(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT followed_username FROM {RELATION_TABLE_FOLLOW} WHERE follower_username = '{username}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
    except Exception:
        return []

def getFollowedUser(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT follower_username FROM {RELATION_TABLE_FOLLOW} WHERE followed_username = '{username}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
    except Exception:
        return []
    
def getuserFollowedPublication(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                        SELECT p.publication_id, p.poster_username, p.description, p.picture, p.created_date, SUM(IF(rp.rating = 0, -1, rp.rating)) AS sum_ratings, rp.rating AS user_rating 
                        FROM {TABLE_PUBLICATION} p 
                        JOIN {RELATION_TABLE_FOLLOW} f ON p.poster_username = f.followed_username
                        LEFT JOIN {RELATION_TABLE_RATE_PUBLICATION} rp ON p.publication_id = rp.publication_id
                        WHERE f.follower_username = '{username}'
                        GROUP BY p.publication_id
                        ORDER BY p.created_date DESC;
                        ''')
        result = cursor.fetchall()
        print(result)
        cursor.close()
        data = []
        
        for row in result:
            post = {
                "publication_id": row[0],
                "poster_id": row[1],
                "description": row[2],
                "picture": row[3],
                "created_date": row[4].strftime('%Y-%m-%d %H:%M:%S'),
                "rating": row[5] if row[5] is not None else 0,
                "user_rating":0 if row[6] is None else (1 if row[6] == b'\x01' else -1)
            }
            data.append(post)
        
        return data
    except Exception as e:
        return None


def getUserByUsernname(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {TABLE_USER} WHERE username = '{username}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(TITLES_USER):
            respond = result[0][x]
            if type(respond) is bytes:
                respond = struct.unpack('<?',respond)[0]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
            if type(respond) is date:
                respond = respond.strftime('%Y-%m-%d')
                
            data[title] = respond
        
        return data
    except Exception as e:
        return None
    
def getAllUser() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {TABLE_USER} ''')
    result = cursor.fetchall()
    
    cursor.close()
    
def getALLFollow() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_FOLLOW} ''')
    result = cursor.fetchall()
    
    cursor.close()
    
