from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def likePublication(publication_id:str, username:str, rating:int) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_RATE_PUBLICATION} 
                       (username, publication_id, rating) 
                       VALUES (
                           "{username}",
                           "{publication_id}",
                           {rating}
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def updateLikePublication(publication_id:str, username:str, rating:bool) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_PUBLICATION} rp
                       SET rp.rating = {rating}
                       WHERE rp.publication_id = "{publication_id}" AND rp.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikePublication(publication_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_PUBLICATION} rp
                       WHERE rp.publication_id = "{publication_id}" and rp.username = "{username}" 
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False