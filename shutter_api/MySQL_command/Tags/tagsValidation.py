from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def doesTagExist(tag:str) -> bool:
    try:
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT value 
                       FROM {TABLE_TAG} 
                       WHERE value = "{tag}"; 
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False