from shutter_api import MYSQL
from shutter_api.Tools import *
from shutter_api.MySQL_command.Comments import *

def createPublication(data:dict) -> bool:
    """
    requete MySQL to create new publication

    Args:
        data (dict):
            "publication_id":str
            "poster_username:str
            "description:str
            "created_date:str

    Returns:
        bool: if request succes
    """
    try:
        picture, file_id = addImgToKitioToPublications(data["picture"], str(data["publication_id"]))
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {TABLE_PUBLICATION} (publication_id, poster_username, description, picture, created_date, file_id) 
                       VALUES (
                           "{data["publication_id"]}",
                           "{data["poster_username"]}",
                           "{data["description"]}",
                           "{picture}",
                           "{data["created_date"]}",
                           "{file_id}"
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deletePublicationFromDB(publication_id:str) -> bool:
    """
    Delete the publication from the data_base

    Args:
        publication_id (str): id of the publication

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f'''
                       SELECT file_id
                       FROM {TABLE_PUBLICATION}
                       WHERE publication_id = "{publication_id}"; 
                       ''')
        file_id = cursor.fetchall()[0][0]
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_PUBLICATION}
                       WHERE publication_id = "{publication_id}"; 
                       ''')
        conn.commit()
        
        deleteImageFromImagekiTio(file_id)
        
        cursor.close()
        return True
    except Exception:
        return False
      
def updatepublication(publication_id:str, description:str) -> bool:
    """
    Update the publication description

    Args:
        publication_id (str): id of the publication
        description (str): new description

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {TABLE_PUBLICATION} p
                       SET p.description = "{description}"
                       WHERE publication_id = "{publication_id}" 
                       ''')
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def getPublicationById(publication_id:str, username:str) -> dict or None:
    """
    get the publication with the id

    Args:
        publication_id (str): id of the publication
        username (str): username of the request

    Returns:
        dict or None : publication data, None if request fail.
    """
    
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                       , get_user_publication_rating("{username}",p.publication_id)
                       FROM publication p
                       LEFT JOIN user u ON p.poster_username = u.username
                       WHERE p.publication_id = "{publication_id}"
                       GROUP BY p.publication_id, p.created_date
                       ORDER BY p.created_date DESC;
                       ''')
        
        row = cursor.fetchall()[0]
        cursor.close()
        
        publication = {
            "publication_id": row[0],
            "poster_user":{
                "username":row[1],
                "profile_picture":row[2]
            },
            "description": row[3],
            "picture":row[4],
            "comments":getCommentsOfPublication(row[0],username=username),
            "nb_comments": getNumberOfCommentsFromPublication(row[0]),
            "created_date": getIntervalOdTimeSinceCreation(row[5]),
            "rating": int(row[6]) if row[6] is not None else 0,
            "tags":getPublicationTags(publication_id),
            "user_rating":getIntFromRating(row[7])
        }
            
        return publication
    except Exception:
        return None
    
def getUserPublications(username:str, offset:int = 1) -> list:
    """
    get The publications of a certain user

    Args:
        username (str): username
        offset (int, optional): foreach offset get the next 10 publications. Defaults to 1.

    Returns:
        list: list of publication of the user
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.publication_id, p.picture, p.created_date
                       FROM publication p
                       WHERE p.poster_username = "{username}"
                       ORDER BY p.created_date DESC
                       LIMIT 12
                       OFFSET {(offset-1) * 12};
                       ''')
        result = cursor.fetchall()
        cursor.close()
        publications = []
        for x in result:
            data = {
                "publication_id": x[0],
                "picture":x[1],
                "created_date":getIntervalOdTimeSinceCreation(x[2])
            }
            publications.append(data)
        
        
        return publications
    except Exception:
        return None
    
def getNumberOfPublicationFromUser(username:str) -> int or None:
    """
    Get the total number of publication of the user

    Args:
        username (str): username

    Returns:
        int or None: number of publication, None if request fail.
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT COUNT(*)
                       FROM publication p
                       WHERE p.poster_username = "{username}"
                       ''')
        result = cursor.fetchall()[0][0]
        cursor.close()
       
        return result
    except Exception:
        return None
     
def getPublicationTags(publication_id:str) -> list:
    """
    Get the tags of a publication

    Args:
        publication_id (str): id of the publication

    Returns:
        list : list of tag link to publication.
    """

    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f"""
                       SELECT i.tag_value
                       FROM {RELATION_TABLE_IDENTIFY} i
                       WHERE i.publication_id = "{publication_id}";
                       """)
        resultat = cursor.fetchall()
        cursor.close()
        
        return [x[0] for x in resultat]
    except Exception:
        return None
    
def removeTagsFromPublication(publication_id:str) -> bool:
    """
    removed tags of a publication

    Args:
        publication_id (str): id of the publication

    Returns:
        bool : if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f"""
                        DELETE FROM {RELATION_TABLE_IDENTIFY}
                        WHERE publication_id = "{publication_id}";
                        """)
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def getNbPublications() -> int or None:
    """
    Get the total number of publicaiton

    Returns:
        int or None: nb of publications, None of request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        cursor.execute(f"""
                       SELECT COUNT(*)
                       FROM {TABLE_PUBLICATION};
                       """)
        result = cursor.fetchall()[0][0]
        cursor.close()
        
        return result
    except Exception:
        return None
    
def getPublicationsFromTag(tag:str,username:str, offset:int= 1) -> list or None:
    """
    get The publications from a certain tag

    Args:
        tag (str): tag of the search
        username (str): username
        offset (int, optional): foreach offset get the next 10 publications. Defaults to 1.

    Returns:
        list or None: list of publication of the user, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT i.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                        , get_user_publication_rating("{username}",p.publication_id)
                        FROM {RELATION_TABLE_IDENTIFY} i
                        LEFT JOIN {TABLE_PUBLICATION} p ON i.publication_id = p.publication_id
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        WHERE i.tag_value = "{tag}"
                        GROUP BY i.publication_id, p.created_date
                        ORDER BY p.created_date DESC
                        LIMIT 12
                        OFFSET {(offset-1) * 12};
                        ''')
        
        result = cursor.fetchall()
        cursor.close()
        data = []
        
        for row in result:
            publication = {
                "publication_id": row[0],
                "poster_user":{
                    "username":row[1],
                    "profile_picture":row[2]
                },
                "description": row[3],
                "picture":row[4],
                "comments":getCommentsOfPublication(row[0],username=username),
                "nb_comments":getNumberOfCommentsFromPublication(row[0]),
                "created_date": getIntervalOdTimeSinceCreation(row[5]),
                "rating": int(row[6]) if row[6] is not None else 0,
                "user_rating": getIntFromRating(row[7]),
                "tags": getPublicationTags(row[0])
                
            }

            
            data.append(publication)
        
        return data
    except Exception:
        return None

def getPublications(username:str, offset:int=1) -> list or None:
    """
    
    get The publications from all publication

    Args:
        username (str): username
        offset (int, optional): foreach offset get the next 10 publications. Defaults to 1.

    Returns:
        list or None: list of publication of the user, None if request fail
    
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                        , get_user_publication_rating("{username}",p.publication_id)
                        FROM {TABLE_PUBLICATION} p
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        GROUP BY p.publication_id, p.created_date
                        ORDER BY p.created_date DESC
                        LIMIT 12
                        OFFSET {(offset-1) * 12};
                        ''')
        
        result = cursor.fetchall()
        cursor.close()
        data = []
        
        for row in result:
            publication = {
                "publication_id": row[0],
                "poster_user":{
                    "username":row[1],
                    "profile_picture":row[2]
                },
                "description": row[3],
                "picture":row[4],
                "comments":getCommentsOfPublication(row[0],username=username),
                "nb_comments":getNumberOfCommentsFromPublication(row[0]),
                "created_date": getIntervalOdTimeSinceCreation(row[5]),
                "rating": int(row[6]) if row[6] is not None else 0,
                "tags":getPublicationTags(row[0])
            }
            if username is not None:
                publication["user_rating"] = getIntFromRating(row[7])
            

            
            data.append(publication)
        
        return data
    except Exception:
        return None
    
def getCommentsOfPublication(publication_id:str, username:str,offset:int = 1) -> list or None:
    """
    get comments from a publication

    Args:
        publication_id (str): publication id
        username (str): user username
        offset (int, optional):foreach offset get the next 10 comments. Defaults to 1.

    Returns:
        list or None: list of comment. None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT c.comment_id, c.commenter_username, u.profile_picture, c.message, c.created_date, c.rating
                        , get_user_comment_rating("{username}",c.comment_id)
                        FROM {TABLE_COMMENT} c 
                        LEFT JOIN {TABLE_USER} u ON c.commenter_username = u.username
                        WHERE c.publication_id = "{publication_id}"
                        GROUP BY c.comment_id, c.created_date
                        ORDER BY c.created_date ASC
                        LIMIT 12
                        OFFSET {(offset-1) * 12};
                        ''')
        
        result = cursor.fetchall()
        
        cursor.close()
        data = []
        
        for row in result:
            comment = {
                "comment_id": row[0],
                "commenter_user":{
                    "username":row[1],
                    "profile_picture":row[2]
                },
                "message": row[3],
                "created_date": getIntervalOdTimeSinceCreation(row[4]),
                "rating": int(row[5]) if row[5] is not None else 0,
            }
            if username is not None:
                comment["user_rating"] = getIntFromRating(row[6])
            data.append(comment)
        
        return data
    except Exception:
        return None