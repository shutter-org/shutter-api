from shutter_api import MYSQL
from .Tools import *


def doesCommentExist(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT c.comment_id 
                       FROM {TABLE_COMMENT} c
                       WHERE c.comment_id = "{comment_id}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def doesCommentBelongToUser(username:str, comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT c.commenter_username
                       FROM {TABLE_COMMENT} c
                       WHERE c.comment_id = "{comment_id}";
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return username == result
    except Exception:
        return False
    
def didUserRateComment(comment_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_RATE_COMMENT} rc
                       WHERE rc.comment_id = "{comment_id}" 
                       AND rc.username = "{username}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def isUserPublicationOwnerFromCommentId(username:str, comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.poster_username
                       FROM {TABLE_COMMENT} c
                       LEFT JOIN {TABLE_PUBLICATION} p ON c.publication_id = p.publication_id
                       WHERE c.comment_id = "{comment_id}";
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return username == result
    except Exception:
        return False
    
def canUserDeleteComment(username:str, comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT c.commenter_username, p.poster_username
                       FROM {TABLE_COMMENT} c
                       LEFT JOIN {TABLE_PUBLICATION} p ON c.publication_id = p.publication_id
                       WHERE c.comment_id = "{comment_id}" 
                       ''')
        row = cursor.fetchall()[0]
        
        cursor.close()
        
        return username == row[0] or username == row[1]
    except Exception:
        return False

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
    
    