from shutter_api import MYSQL
from .Tools import *

def doesPublicationExist(publication_id:str) -> bool:
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
    
def isUsernameCreatorOfPublication(username:str, publication_id:str):
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
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_RATE_PUBLICATION} rp
                       WHERE rp.publication_id = "{publication_id}" AND rp.username = "{username}";
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False

def createPublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {TABLE_PUBLICATION} (publication_id, poster_username, description, picture, created_date) 
                       VALUES (
                           "{data["publication_id"]}",
                           "{data["poster_username"]}",
                           "{data["description"]}",
                           "{data["picture"]}",
                           "{data["created_date"]}"
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deletePublicationFromDB(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_PUBLICATION}
                       WHERE publication_id = "{publication_id}"; 
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def likePublication(publication_id:str, username:str, rating:int) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_RATE_PUBLICATION} 
                       (username, publication_id, rating) 
                       VALUES (
                           "{username}",
                           "{publication_id}",
                           {rating}
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def updatepublication(publication_id:str, description:str) -> bool:
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
    
    
def getPublicationById(publication_id:str, username:str=None) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                       {f""", get_user_publication_rating(u.username,p.publication_id)""" if username is not None else ""}
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
            "created_date": getIntervalOdTimeSinceCreation(row[5]),
            "rating": int(row[6]) if row[6] is not None else 0,
        }
        if username is not None:
            publication["user_rating"] = getIntFromRating(row[7])
            
        publication["tags"] = getPublicationTags(publication_id)
            
        return publication
    except Exception:
        return None
    
def getPublicationTags(publication_id:str) -> list:
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
        return []
    
def removeTagsFromPublication(publication_id:str) -> bool:
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
    
def getPublicationsFromTag(tag:str,username:str = None, offset:int= 1) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT i.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                        {f""", get_user_publication_rating(u.username,p.publication_id)""" if username is not None else ""}
                        FROM {RELATION_TABLE_IDENTIFY} i
                        LEFT JOIN {TABLE_PUBLICATION} p ON i.publication_id = p.publication_id
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        WHERE i.tag_value = "{tag}"
                        GROUP BY i.publication_id, p.created_date
                        ORDER BY p.created_date DESC
                        LIMIT 10
                        OFFSET {(offset-1) * 10};
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
                "created_date": getIntervalOdTimeSinceCreation(row[5]),
                "rating": int(row[6]) if row[6] is not None else 0,
                "tags": getPublicationTags(row[0])
            }
            if username is not None:
                publication["user_rating"] = getIntFromRating(row[7])
            
            data.append(publication)
        
        return data
    except Exception:
        return None

def getPublications(username:str=None, offset:int=1):
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT p.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, p.rating
                        {f""", get_user_publication_rating(u.username,p.publication_id)""" if username is not None else ""}
                        FROM {TABLE_PUBLICATION} p
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        GROUP BY p.publication_id, p.created_date
                        ORDER BY p.created_date DESC
                        LIMIT 10
                        OFFSET {(offset-1) * 10};
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
    
def getCommentsOfPublication(publication_id:str, username:str=None,offset:int = 1):
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT c.comment_id, c.commenter_username, u.profile_picture, c.message, c.created_date, c.rating
                        {f""", get_user_comment_rating(u.username,c.comment_id)""" if username is not None else ""}
                        FROM {TABLE_COMMENT} c 
                        LEFT JOIN {TABLE_USER} u ON c.commenter_username = u.username
                        WHERE c.publication_id = "{publication_id}"
                        GROUP BY c.comment_id, c.created_date
                        ORDER BY c.created_date DESC
                        LIMIT 10
                        OFFSET {(offset-1) * 10};
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
    
def updateLikePublication(publication_id:str, username:str, rating:bool) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_PUBLICATION} rp
                       SET rp.rating = {rating}
                       WHERE rp.publication_id = "{publication_id}" AND rp.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikePublication(publication_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_PUBLICATION} rp
                       WHERE rp.publication_id = "{publication_id}" and rp.username = "{username}" 
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False

