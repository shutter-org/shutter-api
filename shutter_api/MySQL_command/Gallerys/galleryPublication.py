from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def addPublicationToGallery(gallery_id:str, publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_SAVE} 
                       (gallery_id, publication_id) 
                       VALUES (
                           "{gallery_id}",
                           "{publication_id}"
                       );
                       ''')

        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def removePublicationFromGallery(gallery_id:str, publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_SAVE} s
                       WHERE s.gallery_id = "{gallery_id}" 
                       AND s.publication_id = "{publication_id}";
                       ''')
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getGalleryPublications(gallery_Id:str, username:str=None, offset:int = 1) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.publication_id, p.picture
                       FROM {RELATION_TABLE_SAVE} s
                       LEFT JOIN {TABLE_PUBLICATION} p ON s.publication_id = p.publication_id
                       LEFT JOIN {TABLE_GALLERY} g On s.gallery_id = g.gallery_id
                       WHERE s.gallery_id = "{gallery_Id}"
                       AND (g.private = 0 OR (g.private = 1 AND g.creator_username = "{username}")) 
                       ORDER BY p.created_date DESC
                       LIMIT 10
                       OFFSET {(offset-1) * 10};
                       ''')
        result = cursor.fetchall()
        cursor.close()
        
        return [{"publication_id": x[0], "picture":x[1]}for x in result]
    except Exception:
        return []
    