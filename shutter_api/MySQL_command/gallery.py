from shutter_api import MYSQL
from .tableName import *
from .tableTitles import *
from .publication import getPublicationById

def doesGalleryExist(gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT gallery_id FROM {TABLE_GALLERY} WHERE gallery_id = "{gallery_id}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False
    
def doesUserHasAccesToGallery(username:str, gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.private, g.creator_username
                       FROM {TABLE_GALLERY} g
                       WHERE g.gallery_id = "{gallery_id}" ''')
        result = cursor.fetchall()[0]
        cursor.close()
        
        return bool(result[0]) and username == result[1]
    except Exception:
        return False
    
def doesGalleryBelongToUser(username:str, gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.creator_username
                       FROM {TABLE_GALLERY} g
                       WHERE g.gallery_id = "{gallery_id}" ''')
        result = cursor.fetchall()[0][0]
        
        cursor.close()
        
        return username == result
    except Exception:
        return False
    
def didUserRateGallery(gallery_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT * 
                       FROM {RELATION_TABLE_RATE_GALLERY} rg
                       WHERE rg.gallery_id = "{gallery_id}" AND rg.username = "{username}"
                       ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        return len(result) == 1
    except Exception:
        return False

def createGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        
        cursor.execute(f'''INSERT INTO {TABLE_GALLERY} (gallery_id, creator_username, description, created_date, private, title) VALUES (
            "{data["gallery_id"]}",
            "{data["creator_username"]}",
            "{data["description"]}",
            "{data["created_date"]}",
            {data["private"]},
            "{data["title"]}")''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deleteGalleryFromDB(gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_GALLERY} WHERE gallery_id = "{gallery_id}" ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    
def updateGallery(gallery_id:str, description:str = None, title:str = None, private:bool = None) -> bool:
    if description is None and title is None and private is None:
        return False
    
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {TABLE_GALLERY} g
                       SET
                       {f"""g.description = "{description}" """ if description is not None else ""}
                       {f"""{"," if (description is not None) else ""}g.title = "{title}" """ if title is not None else ""}
                       {f"""{"," if (title is not None or description is not None) else ""}g.private = {private} """ if private is not None else ""}
                       WHERE g.gallery_id = "{gallery_id}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
    
def likeGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_RATE_GALLERY} (username, gallery_id, rating) 
                       VALUES ("{data["username"]}","{data["gallery_id"]}",{data["rating"]})
                       ''')
        
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
                       SELECT p.publication_id, p.picture
                       FROM {RELATION_TABLE_SAVE} s
                       LEFT JOIN {TABLE_PUBLICATION} p ON s.publication_id = p.publication_id
                       LEFT JOIN {TABLE_GALLERY} g On s.gallery_id = g.gallery_id
                       WHERE s.gallery_id = "{gallery_Id}"
                       AND (g.private = 0 OR (g.private = 1 AND g.creator_username = "{username}")) 
                       ORDER BY p.created_date DESC
                       LIMIT 10
                       OFFSET {(offset-1) * 10};
                       ''')
        result = cursor.fetchall()
        cursor.close()
        
        return [{"publication_id": x[0], "picture":x[1]}for x in result]
    except Exception:
        return []
    
def getGalleryById(gallery_Id:str, username:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id, g.creator_username, u.profile_picture, g.description, g.created_date, g.rating , 
                       get_user_gallery_rating("{username}",g.gallery_id), g.title
                       FROM {TABLE_GALLERY} g
                       LEFT JOIN {TABLE_USER} u ON g.creator_username = u.username
                       WHERE g.gallery_id = "{gallery_Id}"
                       AND (g.private = 0 OR (g.private = 1 AND g.creator_username = "{username}")) 
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
            "username_rating": 0 if resultGallery[6] is None else (1 if resultGallery[6] == b'\x01' else -1),
            "title": resultGallery[7]
        }

        return data
    except Exception:
        return None
    
    
def addPublicationToGallery(gallery_id:str, publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       INSERT INTO {RELATION_TABLE_SAVE} (gallery_id, publication_id) 
                       VALUES ("{gallery_id}","{publication_id}" )
                       ''')

        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def removePublicationFromGallery(gallery_id:str, publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_SAVE} s
                       WHERE s.gallery_id = "{gallery_id}" and s.publication_id = "{publication_id}" 
                       ''')
        cursor.close()
        conn.commit()
        
        return True
    except ValueError:
        return False
    
def updateLikeGallery(gallery_id:str, username:str, rating:bool) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       UPDATE {RELATION_TABLE_RATE_GALLERY} rg
                       SET rg.rating = {rating}
                       WHERE rg.gallery_id = "{gallery_id}" AND rg.username = "{username}";
                       ''')
        conn.commit()
        cursor.close()
        
        return True
    except Exception:
        return False
    
def deleteLikeGallery(gallery_id:str, username:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {RELATION_TABLE_RATE_GALLERY} rg
                       WHERE rg.gallery_id = "{gallery_id}" and rg.username = "{username}" 
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
    