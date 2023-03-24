from shutter_api import MYSQL
from shutter_api.Tools import TABLE_USER, decrypt
from shutter_api.Keys import SQL_ENCRYPTION_KEY

def isUserPasswordValid(username:str, password:str) -> bool:
    """
    Check for the connection of the username with password

    Args:
        username (str): username
        password (str): password

    Returns:
        bool: if connection succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.password 
                       FROM {TABLE_USER} u 
                       WHERE u.username = "{username}"; 
                       ''')
        result = cursor.fetchall()[0][0]
        cursor.close()
        return decrypt(result,SQL_ENCRYPTION_KEY) == password
    except Exception:
        return False
        
        
