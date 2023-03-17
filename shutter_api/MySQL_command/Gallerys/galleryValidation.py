from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *


def doesGalleryExist(gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT gallery_id 
                       FROM {TABLE_GALLERY} 
                       WHERE gallery_id = "{gallery_id}"; 
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def doesUserHasAccesToGallery(username:str, gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.private, g.creator_username
                       FROM {TABLE_GALLERY} g
                       WHERE g.gallery_id = "{gallery_id}"; 
                       ''')
        result = cursor.fetchall()[0]
        cursor.close()
        
        return bool(result[0]) and username == result[1]
    except Exception:
        return False
    
def doesGalleryBelongToUser(username:str, gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.creator_username
                       FROM {TABLE_GALLERY} g
                       WHERE g.gallery_id = "{gallery_id}"; 
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return username == result
    except Exception:
        return False
    
def didUserRateGallery(gallery_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_RATE_GALLERY} rg
                       WHERE rg.gallery_id = "{gallery_id}" 
                       AND rg.username = "{username}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False