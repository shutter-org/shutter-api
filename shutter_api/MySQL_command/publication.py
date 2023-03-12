from shutter_api import MYSQL
import struct
from datetime import datetime
from .tableName import *
from .tableTitles import *

def doesPublicationExist(publication_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT publication_id FROM {TABLE_PUBLICATION} WHERE publication_id = '{publication_id}' ''')
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
        
        cursor.execute(f'''DELETE FROM {TABLE_PUBLICATION} WHERE publication_id = '{publication_id}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        return False
    
def likePublication(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_RATE_PUBLICATION} (username, publication_id, rating) VALUES (
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
        
        cursor.execute(f'''SELECT * FROM {TABLE_PUBLICATION} WHERE publication_id = '{publication_id}' ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(TITLES_PUBLICATION):
            respond = result[0][x]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
                
            data[title] = respond
        return data
    except Exception as e:
        return None
    
def getCommentsOfPublication(publication_id:str, username:str=None):
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                        SELECT c.comment_id, c.commenter_username, c.message, c.created_date, SUM(IF(rc.rating = 0, -1, rc.rating)) AS sum_ratings{f""", rc.rating AS user_rating""" if username is not None else ""}
                        FROM {TABLE_COMMENT} c 
                        LEFT JOIN {RELATION_TABLE_RATE_COMMENT} rc ON c.comment_id = rc.comment_id
                        {f"""LEFT JOIN {RELATION_TABLE_RATE_COMMENT} urc ON c.comment_id = rc.comment_id AND urc.username = '{username}'""" if username is not None else ""}
                        WHERE c.publication_id = '{publication_id}'
                        GROUP BY c.comment_id
                        ORDER BY c.created_date DESC;
                        ''')
        
        result = cursor.fetchall()
        cursor.close()
        data = []
        
        for row in result:
            comment = {
                "comment_id": row[0],
                "commenter_username": row[1],
                "message": row[2],
                "created_date": row[3].strftime('%Y-%m-%d %H:%M:%S'),
                "rating": row[4] if row[4] is not None else 0,
            }
            if username is not None:
                comment["user_rating"] = row[5] if row[5] is None else struct.unpack('<?',row[5])[0]
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
    
    cursor.execute(f'''SELECT * FROM {RELATION_TABLE_RATE_PUBLICATION} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()