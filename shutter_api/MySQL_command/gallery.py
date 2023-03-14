from shutter_api import MYSQL
import struct
from .tableName import *
from .tableTitles import *
from .publication import getPublicationById

def createGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        
        cursor.execute(f'''INSERT INTO {TABLE_GALLERY} (gallery_id, creator_username, description, created_date, private) VALUES (
            "{data["gallery_id"]}",
            "{data["creator_username"]}",
            "{data["description"]}",
            "{data["created_date"]}",
            {data["private"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deleteGalleryFromDB(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_GALLERY} WHERE gallery_id = "{comment_id}" ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def likeGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_RATE_GALLERY} (username, gallery_id, rating) VALUES (
            "{data["username"]}",
            "{data["gallery_id"]}",
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getGalleryPublications(gallery_Id:str, username:str=None, offset:int = 1) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT p.publication_id
                       FROM {RELATION_TABLE_SAVE} s
                       LEFT JOIN {TABLE_PUBLICATION} p ON s.publication_id = p.publication_id
                       WHERE s.gallery_id = "{gallery_Id}"
                       ORDER BY p.created_date DESC
                       LIMIT 10
                       OFFSET {(offset-1) * 10};
                       ''')
        result = cursor.fetchall()
        print(result)
        cursor.close()
        
        return [getPublicationById(x[0],username) for x in result]
    except Exception:
        return []
    
def getGalleryById(gallery_Id:str, username:str, offset:int = 1) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id, g.creator_username, u.profile_picture, g.description, g.created_date, SUM(CASE WHEN rg.rating = 1 THEN 1 WHEN rg.rating = 0 THEN -1 ELSE 0 END) , rg.rating
                       FROM {TABLE_GALLERY} g
                       LEFT JOIN {RELATION_TABLE_RATE_GALLERY} rg ON g.gallery_id = rg.gallery_id
                       LEFT JOIN {TABLE_USER} u ON g.creator_username = u.username
                       LEFT JOIN {RELATION_TABLE_RATE_GALLERY} urg ON g.gallery_id = urg.gallery_id AND urg.username = "{username}"
                       WHERE g.gallery_id = "{gallery_Id}"
                       AND (g.private = 0 OR (g.private = 1 AND g.creator_username = "{username}")) 
                       GROUP BY g.gallery_id
                       ORDER BY g.created_date DESC;
                       ''')
        resultGallery = cursor.fetchall()[0]

        cursor.close()
        
        data = {
            "gallery_id": resultGallery[0],
            "creator_user":{
                "username":resultGallery[1],
                "profile_picture":resultGallery[2]
            },
            "description": resultGallery[3],
            "created_date": resultGallery[4].strftime('%Y-%m-%d %H:%M:%S'),
            "rating": int(resultGallery[5]),
            "publications":getGalleryPublications(gallery_Id,username=username),
            "username_rating": 0 if resultGallery[6] is None else (1 if resultGallery[6] == b'\x01' else -1)
        }

        return data
    except Exception:
        return None
    
    
def addPublicationToGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''INSERT INTO {RELATION_TABLE_SAVE} (gallery_id, publication_id) VALUES (
            "{data["gallery_id"]}",
            "{data["publication_id"]}" 
            )''')

        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getAllGallery() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {TABLE_GALLERY} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRateGallery() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_RATE_GALLERY} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllSave() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_SAVE} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()