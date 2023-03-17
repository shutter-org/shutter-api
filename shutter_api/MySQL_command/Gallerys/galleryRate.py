from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def likeGallery(gallery_id, username, rating) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_RATE_GALLERY} 
                       (username, gallery_id, rating) 
                       VALUES (
                           "{username}",
                           "{gallery_id}",
                           {rating}
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def updateLikeGallery(gallery_id:str, username:str, rating:bool) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_GALLERY} rg
                       SET rg.rating = {rating}
                       WHERE rg.gallery_id = "{gallery_id}" 
                       AND rg.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikeGallery(gallery_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_GALLERY} rg
                       WHERE rg.gallery_id = "{gallery_id}" 
                       AND rg.username = "{username}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    