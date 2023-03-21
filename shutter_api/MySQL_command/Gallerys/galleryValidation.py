from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *


def doesGalleryExist(gallery_id:str) -> bool:
    """
    Check if the gallery exist

    Args:
        gallery_id (str): gallery id

    """
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
    """
    Check if the users has accest to the private gallerys

    Args:
        username (str): user username
        gallery_id (str): gallery id

    """
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
        return not bool(result[0]) or username == result[1]
    except Exception:
        return False
    
def doesGalleryBelongToUser(username:str, gallery_id:str) -> bool:
    """
    Check if the username is the creator of the gallery

    Args:
        username (str): user username
        gallery_id (str): gallery id

    """
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
    """
    Check if the user already rated the gallery

    Args:
        gallery_id (str): gallery id
        username (str): user username
    """
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