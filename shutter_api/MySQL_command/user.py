from shutter_api import MYSQL
import struct
from datetime import datetime, date
from .tableName import *
from .tableTitles import *

def doesUsernameExist(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT username FROM {USER_TABLE_NAME} WHERE username = '{userName}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT email FROM {USER_TABLE_NAME} WHERE email = '{email}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 0
    except Exception:
        return False

def deleteUserFromDB(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {USER_TABLE_NAME} WHERE username = '{userName}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def usernameFollowUser(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {FOLLOW_RELATION_TABLE_NAME} (follower_username, followed_username) VALUES (
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
        
        cursor.execute(f'''SELECT followed_username FROM {FOLLOW_RELATION_TABLE_NAME} WHERE follower_username = '{username}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        return [x[0] for x in result]
    except Exception:
        return []

def getFollowedUser(username:str) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT follower_username FROM {FOLLOW_RELATION_TABLE_NAME} WHERE followed_username = '{username}' ''')
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
                       SELECT *
                       FROM {PUBLICATION_TABLE_NAME}
                       WHERE poster_username IN  (
                           SELECT followed_username
                           FROM follow
                           WHERE follower_username = '{username}')''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        for respond in result:
            post = {}
            for x,title in enumerate(PUBLICATION_TITLES):
                tempo = respond[x]
                if type(tempo) is datetime:
                    tempo = tempo.strftime('%Y-%m-%d %H:%M:%S')
                    
                post[title] = tempo

            data.append(post)
        
        return data
    except Exception as e:
        return None


def getUserByUsernname(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {USER_TABLE_NAME} WHERE username = '{username}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(USER_TITLES):
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
    
    cursor.execute(f'''SELECT * FROM {USER_TABLE_NAME} ''')
    result = cursor.fetchall()
    
    cursor.close()
    
def getALLFollow() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {FOLLOW_RELATION_TABLE_NAME} ''')
    result = cursor.fetchall()
    
    cursor.close()
    
