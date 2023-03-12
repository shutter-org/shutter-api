from shutter_api import MYSQL
from .tableTitles import *
from .tableName import *

def createNewUser(data:dict) -> bool:
    
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_USER} (username, password, email, name, biography, created_date, birthdate) VALUES (
            '{data["username"]}',
            '{data["password"]}',
            '{data["email"]}',
            '{data["name"]}',
            '{data["biography"]}',
            '{data["created_date"]}',
            '{data["birthdate"]}')''')
        cursor.close()
        conn.commit()
    except Exception:
        return False
    finally:
        return True
