from shutter_api import MYSQL
import struct
from datetime import datetime
from .tableName import *
from .tableTitles import *

def doesPublicationExist(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT publication_id FROM {TABLE_PUBLICATION} WHERE publication_id = "{publication_id}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False

def createPublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_PUBLICATION} (publication_id, poster_username, description, picture, created_date) VALUES (
            "{data["publication_id"]}",
            "{data["poster_username"]}",
            "{data["description"]}",
            "{data["picture"]}",
            "{data["created_date"]}")''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deletePublicationFromDB(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_PUBLICATION} WHERE publication_id = "{publication_id}" ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def likePublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_RATE_PUBLICATION} (username, publication_id, rating) VALUES (
            "{data["username"]}",
            "{data["publication_id"]}",
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getPublicationById(publication_id:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {TABLE_PUBLICATION} WHERE publication_id = "{publication_id}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(TITLES_PUBLICATION):
            respond = result[0][x]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
                
            data[title] = respond
        return data
    except Exception:
        return None
    
def getPublicationsFromTag(tag:str,username:str = None, offset:int= 1) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT i.publication_id, p.poster_username, u.profile_picture, p.description, p.picture, p.created_date, SUM(CASE WHEN rp.rating = 1 THEN 1 WHEN rp.rating = 0 THEN -1 ELSE 0 END){f""", urp.rating""" if username is not None else ""}
                        FROM {RELATION_TABLE_IDENTIFY} i
                        LEFT JOIN {TABLE_PUBLICATION} p ON i.publication_id = p.publication_id
                        LEFT JOIN {RELATION_TABLE_RATE_PUBLICATION} rp ON i.publication_id = rp.publication_id
                        LEFT JOIN {TABLE_USER} u ON p.poster_username = u.username
                        {f"""LEFT JOIN {RELATION_TABLE_RATE_PUBLICATION} urp ON p.publication_id = urp.publication_id AND urp.username = "{username}" """ if username is not None else ""}
                        WHERE i.tag_value = "{tag}"
                        GROUP BY i.publication_id
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
                "created_date": row[5].strftime('%Y-%m-%d %H:%M:%S'),
                "rating": int(row[6]) if row[6] is not None else 0,
            }
            if username is not None:
                publication["user_rating"] = 0 if row[7] is None else (1 if row[7] == b'\x01' else -1)
            

            
            data.append(publication)
        
        return data
    except ValueError:
        return None

def getPublications(username:str=None, offset:int=1):
    pass
    
def getCommentsOfPublication(publication_id:str, username:str=None,offset:int = 1):
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT c.comment_id, c.commenter_username, u.profile_picture, c.message, c.created_date, SUM(CASE WHEN rc.rating = 1 THEN 1 WHEN rc.rating = 0 THEN -1 ELSE 0 END){f""", urc.rating""" if username is not None else ""}
                        FROM {TABLE_COMMENT} c 
                        LEFT JOIN {RELATION_TABLE_RATE_COMMENT} rc ON c.comment_id = rc.comment_id
                        LEFT JOIN {TABLE_USER} u ON c.commenter_username = u.username
                        {f"""LEFT JOIN {RELATION_TABLE_RATE_COMMENT} urc ON c.comment_id = urc.comment_id AND urc.username = "{username}" """ if username is not None else ""}
                        WHERE c.publication_id = "{publication_id}"
                        GROUP BY c.comment_id
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
                "created_date": row[4].strftime('%Y-%m-%d %H:%M:%S'),
                "rating": int(row[5]) if row[5] is not None else 0,
            }
            if username is not None:
                comment["user_rating"] = 0 if row[6] is None else (1 if row[6] == b'\x01' else -1)
            data.append(comment)
        
        return data
    except Exception:
        return None

    
def getAllPublication() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {TABLE_PUBLICATION} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRatePublication() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    print("ok")
    cursor.execute(f'''SELECT * 
                   FROM {RELATION_TABLE_RATE_PUBLICATION}
                   ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
