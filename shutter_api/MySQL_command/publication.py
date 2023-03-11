from shutter_api import MYSQL
from datetime import datetime
from .tableName import *
from .tableTitles import *

def createPublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {PUBLICATION_TABLE_NAME} (publication_id, poster_username, description, picture, created_date) VALUES (
            '{data["publication_id"]}',
            '{data["poster_username"]}',
            '{data["description"]}',
            '{data["picture"]}',
            '{data["created_date"]}')''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def deletePublicationFromDB(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {PUBLICATION_TABLE_NAME} WHERE publication_id = '{publication_id}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        return False
    
def likePublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RATE_PUBLICATION_RELATION_TABLE_NAME} (username, publication_id, rating) VALUES (
            '{data["username"]}',
            '{data["publication_id"]}',
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def getPublicationById(publication_id:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {PUBLICATION_TABLE_NAME} WHERE publication_id = '{publication_id}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(PUBLICATION_TITLES):
            respond = result[0][x]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
                
            data[title] = respond
        return data
    except Exception as e:
        return None
    
    
def getAllPublication() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    print("ok")
    cursor.execute(f'''SELECT * FROM {PUBLICATION_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRatePublication() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RATE_PUBLICATION_RELATION_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()