from shutter_api import MYSQL
from .tableName import *
from .tableTitles import *

def createComment(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {COMMENT_TABLE_NAME} (comment_id, commenter_username, publication_id, message, created_date) VALUES (
            '{data["comment_id"]}',
            '{data["commenter_username"]}',
            '{data["publication_id"]}',
            '{data["message"]}',
            '{data["created_date"]}')''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def deleteCommentFromDB(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {COMMENT_TABLE_NAME} WHERE comment_id = '{comment_id}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        return False
    
def likeComment(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RATE_COMMENT_RELATION_TABLE_NAME} (username, comment_id, rating) VALUES (
            '{data["username"]}',
            '{data["comment_id"]}',
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def getAllComment() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {COMMENT_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRateComment() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * FROM {RATE_COMMENT_RELATION_TABLE_NAME} ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()