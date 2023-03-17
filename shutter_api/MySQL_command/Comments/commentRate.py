from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *

def likeComment(comment_id:set, username:str, rating:int) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_RATE_COMMENT}
                       (username, comment_id, rating) 
                       VALUES (
                           "{username}",
                           "{comment_id}",
                           {rating}
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def updateLikeComment(comment_id:str, username:str, rating:bool) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_COMMENT} rc
                       SET rc.rating = {rating}
                       WHERE rc.comment_id = "{comment_id}" 
                       AND rc.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikeComment(comment_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_COMMENT} rc
                       WHERE rc.comment_id = "{comment_id}" 
                       AND rc.username = "{username}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    