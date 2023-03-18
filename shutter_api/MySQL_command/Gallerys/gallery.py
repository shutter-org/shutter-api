from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *
from .galleryPublication import getGalleryPublications


def createGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        
        cursor.execute(f'''INSERT INTO {TABLE_GALLERY} 
                       (gallery_id, creator_username, description, created_date, private, title) 
                       VALUES (
                           "{data["gallery_id"]}",
                           "{data["creator_username"]}",
                           "{data["description"]}",
                           "{data["created_date"]}",
                           {data["private"]},
                           "{data["title"]}"
                       );
                       ''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def deleteGalleryFromDB(gallery_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_GALLERY} 
                       WHERE gallery_id = "{gallery_id}"; 
                       ''')
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

def getNumberPublicationsFromGallery(gallery_id:str) -> int or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT COUNT(*)
                       FROM {RELATION_TABLE_SAVE} s
                       WHERE s.gallery_id = "{gallery_id}";
                       ''')
        result = cursor.fetchall()[0][0]

        cursor.close()
       
        return result
    except Exception:
        return None

def getGalleryById(gallery_id:str, username:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id, g.creator_username, u.profile_picture, g.description, g.created_date, g.rating , 
                       get_user_gallery_rating("{username}",g.gallery_id), g.title
                       FROM {TABLE_GALLERY} g
                       LEFT JOIN {TABLE_USER} u ON g.creator_username = u.username
                       WHERE g.gallery_id = "{gallery_id}"
                       AND (g.private = 0 OR (g.private = 1 AND g.creator_username = "{username}")) 
                       ORDER BY g.created_date DESC;
                       ''')
        row = cursor.fetchall()[0]

        cursor.close()
        
        data = {
            "gallery_id": row[0],
            "creator_user":{
                "username":row[1],
                "profile_picture":row[2]
            },
            "description": row[3],
            "created_date": getIntervalOdTimeSinceCreation(row[4]),
            "rating": int(row[5]),
            "publications":getGalleryPublications(gallery_id,username=username),
            "nb_publication":getNumberPublicationsFromGallery(gallery_id),
            "username_rating": getIntFromRating(row[6]),
            "title": row[7]
        }

        return data
    except Exception:
        return None