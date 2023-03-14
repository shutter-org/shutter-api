from shutter_api import MYSQL
from .tableName import *

def createTag(tag:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_TAG} (value) VALUES ("{tag}")''')
        
        cursor.close()
        conn.commit()
        return True
    
    except Exception:
        return False

        
    
def doesTagExist(tag:str) -> bool:
    try:
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT value FROM {TABLE_TAG} WHERE value = "{tag}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def addTagToPublication(tag:str, publication_id:str) -> bool:
    try:
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_IDENTIFY} (publication_id, tag_value) VALUES ("{publication_id}", "{tag}")''')
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getAllTags() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {TABLE_TAG}''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllIdentify() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_IDENTIFY}''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
