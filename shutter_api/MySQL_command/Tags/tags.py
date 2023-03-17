from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def createTag(tag:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {TABLE_TAG} 
                       (value) 
                       VALUES 
                       ("{tag}");
                       ''')
        
        cursor.close()
        conn.commit()
        return True
    
    except Exception:
        return False
    
def addTagToPublication(tag:str, publication_id:str) -> bool:
    try:
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_IDENTIFY} 
                       (publication_id, tag_value) 
                       VALUES 
                       ("{publication_id}", "{tag}");
                       ''')
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
