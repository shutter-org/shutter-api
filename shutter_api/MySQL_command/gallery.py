from shutter_api import MYSQL
import struct
from datetime import datetime
from .tableName import *
from .tableTitles import *

def createGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {GALLERY_TABLE_NAME} (gallery_id, creator_username, description, created_date, private) VALUES (
            '{data["gallery_id"]}',
            '{data["creator_username"]}',
            '{data["description"]}',
            '{data["created_date"]}',
            {data["private"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def deleteGalleryFromDB(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {GALLERY_TABLE_NAME} WHERE gallery_id = '{comment_id}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        return False
    
def likeGallery(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RATE_GALLEY_RELATION_TABLE_NAME} (username, gallery_id, rating) VALUES (
            '{data["username"]}',
            '{data["gallery_id"]}',
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def getGalleryById(gallery_Id:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {GALLERY_TABLE_NAME} WHERE gallery_id = '{gallery_Id}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(GALLERY_TITLES):
            respond = result[0][x]
            if type(respond) is bytes:
                respond = struct.unpack('<?',respond)[0]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
                
            data[title] = respond
        return data
    except Exception as e:
        return None
    
def addPublicationToGallery(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        """
        cursor.execute(f'''INSERT INTO rate_gallery (username, gallery_id, rating) VALUES (
            '{data["username"]}',
            '{data["gallery_id"]}',
            {data["rating"]})''')
        """
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
def getAllGallery() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {GALLERY_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRateGallery() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RATE_GALLEY_RELATION_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()