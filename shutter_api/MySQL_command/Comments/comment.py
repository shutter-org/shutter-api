from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *


def getCommentById(comment_id:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {TABLE_COMMENT} 
                       WHERE comment_id = "{comment_id}";
                       ''')
        row = cursor.fetchall()[0]
        
        cursor.close()
        
        data = {
            "comment_id": row[0],
            "commenter_username": row[1],
            "publication_id": row[2],
            "message": row[3],
            "created_date": getIntervalOdTimeSinceCreation(row[4]),
            "rating":row[5]
        }

        return data
    except Exception:
        return None

def createComment(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_COMMENT} (comment_id, commenter_username, publication_id, message, created_date) VALUES (
            "{data["comment_id"]}",
            "{data["commenter_username"]}",
            "{data["publication_id"]}",
            "{data["message"]}",
            "{data["created_date"]}")''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deleteCommentFromDB(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_COMMENT} 
                       WHERE comment_id = "{comment_id}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def updateComment(comment_id:str, message:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {TABLE_COMMENT} c
                       SET c.message = "{message}"
                       WHERE c.comment_id = "{comment_id}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def getNumberOfCommentsFromPublication(publication_id:str) -> int or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT COUNT(*) 
                       FROM {TABLE_COMMENT} c
                       WHERE c.publication_id = "{publication_id}";
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return result
    except Exception:
        return None