from shutter_api import MYSQL
from shutter_api.Tools import *

def doesCommentExist(comment_id:str) -> bool:
    """
    Check if the comment exist in the DB

    Args:
        comment_id (str): _description_

    Returns:
        bool: _description_
    """
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
    """
    Check if the comment belong to the user

    Args:
        username (str): user username
        comment_id (str): comment id

    """
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
    """
    Check if the user already rated the comment

    Args:
        comment_id (str): comment id
        username (str): user username
    """
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
    """
    Check if the user is the creator of the publication in witch the comment belong

    Args:
        username (str): user username
        comment_id (str): comment id

    """
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
    """
    Check if the user has privilege to delete a comment

    Args:
        username (str): user username
        comment_id (str): comment id

    """
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
