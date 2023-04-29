from shutter_api import MYSQL
from shutter_api.Tools import *


def getCommentById(comment_id: str) -> dict or None:
    """
    Get a specific comment data

    Args:
        comment_id (str): comment id

    Returns:
        dict or None: comment data, None id request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT * 
                       FROM {TABLE_COMMENT} 
                       WHERE comment_id = '{comment_id}';
                       ''')
        row = cursor.fetchall()[0]

        cursor.close()

        data = {
            "comment_id": row[0],
            "commenter_username": row[1],
            "publication_id": row[2],
            "message": row[3],
            "created_date": getIntervalOdTimeSinceCreation(row[4]),
            "rating": row[5]
        }

        return data
    except Exception:
        return None


def createComment(data: dict) -> bool:
    """
    Create a new comment

    Args:
        data (dict): 
            comment_id: str
            commenter_username: str
            publication_id: str
            message: str
            created_date: str

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''INSERT INTO {TABLE_COMMENT} (comment_id, commenter_username, publication_id, message, created_date) VALUES (
            '{data["comment_id"]}',
            '{data["commenter_username"]}',
            '{data["publication_id"]}',
            '{data["message"]}',
            '{data["created_date"]}')''')

        cursor.close()
        conn.commit()

        return True
    except Exception:
        return False


def deleteCommentFromDB(comment_id: str) -> bool:
    """
    Remove a comment form the DB

    Args:
        comment_id (str): comment id

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       DELETE FROM {TABLE_COMMENT} 
                       WHERE comment_id = '{comment_id}';
                       ''')
        conn.commit()

        cursor.close()
        return True
    except Exception:
        return False


def updateComment(comment_id: str, message: str) -> bool:
    """
    Update a comment message

    Args:
        comment_id (str): comment id
        message (str): new message

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       UPDATE {TABLE_COMMENT} c
                       SET c.message = '{message}'
                       WHERE c.comment_id = '{comment_id}';
                       ''')
        conn.commit()

        cursor.close()
        return True
    except Exception:
        return False


def getNumberOfCommentsFromPublication(publication_id: str) -> int or None:
    """
    Get the total number of comment of a publication

    Args:
        publication_id (str): publication id

    Returns:
        int or None: number of comments, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT COUNT(*) 
                       FROM {TABLE_COMMENT} c
                       WHERE c.publication_id = '{publication_id}';
                       ''')
        result = cursor.fetchall()[0][0]

        cursor.close()

        return result
    except Exception:
        return None
