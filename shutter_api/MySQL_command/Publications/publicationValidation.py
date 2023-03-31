from shutter_api import MYSQL
from shutter_api.Tools import *

def doesPublicationExist(publication_id:str) -> bool:
    """
    check if publication exist

    Args:
        publication_id (str): publication_id

    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT publication_id 
                       FROM {TABLE_PUBLICATION} 
                       WHERE publication_id = "{publication_id}"; 
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def isUsernameCreatorOfPublication(username:str, publication_id:str) -> bool:
    """
    Check if the username is the creator of the publication

    Args:
        username (str): user username
        publication_id (str): publication publication_id
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT poster_username 
                       FROM {TABLE_PUBLICATION} 
                       WHERE publication_id = "{publication_id}" ''')
        
        resultat = cursor.fetchall()[0][0]
        cursor.close()
        
        return resultat == username
    except Exception:
        return False
    
def doesPublicationBelongToUser(username:str, publication_id:str) -> bool:
    """
    check if publicaiton belong to the user

    Args:
        username (str): user username
        publication_id (str): _description_

    Returns:
        bool: _description_
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.poster_username
                       FROM {TABLE_PUBLICATION} p
                       WHERE p.publication_id = "{publication_id}"; 
                       ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return username == result
    except Exception:
        return False
    
def didUserRatePublication(publication_id:str, username:str) -> bool:
    """
    Check if username already rated a publication

    Args:
        publication_id (str): publication publication_id
        username (str): user username

    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_RATE_PUBLICATION} rp
                       WHERE rp.publication_id = "{publication_id}" AND BINARY rp.username = "{username}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
