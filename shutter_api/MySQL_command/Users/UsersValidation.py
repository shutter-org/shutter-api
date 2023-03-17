from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *


def doesUsernameExist(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT username 
                       FROM {TABLE_USER} 
                       WHERE username = "{userName}"; 
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT email 
                       FROM {TABLE_USER} 
                       WHERE email = "{email}"; 
                       ''')
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