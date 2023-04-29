from shutter_api import MYSQL
from shutter_api.Tools import *


def addPublicationToGallery(gallery_id: str, publication_id: str) -> bool:
    """
    Add a publication to a gallery

    Args:
        gallery_id (str): gallery id
        publication_id (str): publication id

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_SAVE} 
                       (gallery_id, publication_id) 
                       VALUES (
                           '{gallery_id}',
                           '{publication_id}'
                       );
                       ''')

        cursor.close()
        conn.commit()

        return True
    except Exception:
        return False


def removePublicationFromGallery(gallery_id: str, publication_id: str) -> bool:
    """
    Remove a publication from a gallery

    Args:
        gallery_id (str): gallery id
        publication_id (str): publication id

    Returns:
        bool: if request success
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_SAVE} s
                       WHERE s.gallery_id = '{gallery_id}' 
                       AND s.publication_id = '{publication_id}';
                       ''')
        cursor.close()
        conn.commit()

        return True
    except Exception:
        return False


def getGalleryPublications(gallery_Id: str, username: str, offset: int = 1) -> list or None:
    """
    Get the publications of a gallery by batch of 10

    Args:
        gallery_Id (str): gallery if
        username (str): user username. Defaults to None.
        offset (int, optional): foreach offset give the 10 new publications. Defaults to 1.

    Returns:
        list or None: list if publications, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT p.publication_id, p.picture
                       FROM {RELATION_TABLE_SAVE} s
                       LEFT JOIN {TABLE_PUBLICATION} p ON s.publication_id = p.publication_id
                       LEFT JOIN {TABLE_GALLERY} g On s.gallery_id = g.gallery_id
                       WHERE s.gallery_id = '{gallery_Id}'
                       AND (g.private = 0 OR (g.private = 1 AND BINARY g.creator_username = '{username}')) 
                       ORDER BY p.created_date DESC
                       LIMIT 12
                       OFFSET {(offset - 1) * 12};
                       ''')
        result = cursor.fetchall()
        cursor.close()

        return [{"publication_id": x[0], "picture": x[1]} for x in result]
    except Exception:
        return None
