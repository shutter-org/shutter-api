from shutter_api import MYSQL
from shutter_api.Tools import *

def likeComment(comment_id:set, username:str, rating:bool) -> bool:
    """
    Add the rating of a user to a comment

    Args:
        comment_id (set): comment id
        username (str): user username
        rating (bool): rating of the user

    Returns:
        bool: if request succes
    """
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
    """
    Change the rating of a user

    Args:
        comment_id (str): comment id
        username (str): user username
        rating (bool): new user rating

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_COMMENT} rc
                       SET rc.rating = {rating}
                       WHERE rc.comment_id = "{comment_id}" 
                       AND BINARY rc.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikeComment(comment_id:str, username:str) -> bool:
    """
    Remove the rating of a user on a comment

    Args:
        comment_id (str): comment id
        username (str): user username

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_COMMENT} rc
                       WHERE rc.comment_id = "{comment_id}" 
                       AND BINARY rc.username = "{username}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    