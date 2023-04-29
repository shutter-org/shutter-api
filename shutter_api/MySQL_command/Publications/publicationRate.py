from shutter_api import MYSQL
from shutter_api.Tools import *


def likePublication(publication_id: str, username: str, rating: bool) -> bool:
    """
    Add user rating to db

    Args:
        publication_id (str): publication id
        username (str): user username
        rating (bool): user rating

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_RATE_PUBLICATION} 
                       (username, publication_id, rating) 
                       VALUES (
                           '{username}',
                           '{publication_id}',
                           {rating}
                       );
                       ''')

        cursor.close()
        conn.commit()

        return True
    except Exception:
        return False


def updateLikePublication(publication_id: str, username: str, rating: bool) -> bool:
    """
    Change user publication rating

    Args:
        publication_id (str): publication id
        username (str): user username
        rating (bool): new rating

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_PUBLICATION} rp
                       SET rp.rating = {rating}
                       WHERE rp.publication_id = '{publication_id}' AND BINARY rp.username = '{username}';
                       ''')
        conn.commit()
        cursor.close()

        return True
    except Exception:
        return False


def deleteLikePublication(publication_id: str, username: str) -> bool:
    """
    remove user publication rating

    Args:
        publication_id (str): publication id
        username (str): user username

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_PUBLICATION} rp
                       WHERE rp.publication_id = '{publication_id}' and BINARY rp.username = '{username}' 
                       ''')
        conn.commit()

        cursor.close()
        return True
    except Exception:
        return False
