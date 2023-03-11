from shutter_api import MYSQL
from .tableName import *
from .tableTitles import *

def isUserPasswordValid(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT password FROM {USER_TABLE_NAME} WHERE username = '{data["username"]}' ''')
        result = cursor.fetchall()[0][0]
        cursor.close()
        
        return result == data["password"]
    except Exception:
        return False
        
        
