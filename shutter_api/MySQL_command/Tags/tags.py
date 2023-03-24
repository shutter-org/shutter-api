from shutter_api import MYSQL
from shutter_api.Tools import *

def createTag(tag:str) -> bool:
    """
    Create a new tafg
    Args:
        tag (str): new tag

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {TABLE_TAG} 
                       (value) 
                       VALUES 
                       ("{tag}");
                       ''')
        
        cursor.close()
        conn.commit()
        return True
    
    except Exception:
        return False
    
def addTagToPublication(tag:str, publication_id:str) -> bool:
    """
    link a tag to a publication

    Args:
        tag (str): new tag
        publication_id (str): publication_id

    Returns:
        bool: if request succes
    """
    try:
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_IDENTIFY} 
                       (publication_id, tag_value) 
                       VALUES 
                       ("{publication_id}", "{tag}");
                       ''')
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getNbpublicationFromTag(tag:str) -> int or None:
    """
    get the number of publicaiton related to this tag

    Args:
        tag (str): tag

    Returns:
        int or None: number of publications, if None request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT t.nb_publications
                       FROM {TABLE_TAG} t
                       WHERE t.value = "{tag}"
                       ''')
        result = cursor.fetchall()[0][0]
        cursor.close()
       
        return result
    except Exception:
        return None
    
def getTags(search:str) -> list or None:
    """
    get tags base on the search param

    Args:
        search (str): search keyword

    Returns:
        list or None: list of tag, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT t.value, t.nb_publications
                       FROM {TABLE_TAG} t
                       WHERE t.value LIKE '{search}%'
                       ORDER BY t.nb_publications DESC
                       LIMIT 12;
                       ''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        for row in result:
            data.append({
                "tag":row[0],
                "nb_publications":row[1]
            })
        
        
        return data
    except Exception:
        return None