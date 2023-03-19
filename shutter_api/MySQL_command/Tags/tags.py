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
    
def getTags(search:str) -> list or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT t.value, t.nb_publications
                       FROM {TABLE_TAG} t
                       WHERE t.value LIKE '{search}%'
                       ORDER BY t.nb_publications DESC
                       LIMIT 10;
                       ''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        for row in result:
            data.append({
                "tag":row[0],
                "nb_publication":row[1]
            })
        
        
        return data
    except ValueError:
        return None