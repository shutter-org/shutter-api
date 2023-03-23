from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *


def doesUsernameExist(username:str) -> bool:
    """
    Check if username existe

    Args:
        username (str): user username

    """
    print("ok1")
    try:
        conn = MYSQL.get_db()
        print("ok2")
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT username 
                       FROM {TABLE_USER} 
                       WHERE username = "{username}"; 
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    

def isEmailValid(email:str) -> bool:
    """
    if email is available

    Args:
        email (str): user email

    """
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
    
def doesUserFollowUsername(follower:str, followed:str) -> bool:
    """
    check if user follow another user

    Args:
        follower (str): user username
        followed (str): username of the other username

    """
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