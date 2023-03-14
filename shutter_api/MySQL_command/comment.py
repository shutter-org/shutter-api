from shutter_api import MYSQL
from .tableName import *
from .tableTitles import *
from datetime import datetime

def getCommentById(comment_id:str) -> dict or None:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''SELECT * FROM {TABLE_COMMENT} WHERE comment_id = "{comment_id}" ''')
        result = cursor.fetchall()
        
        cursor.close()
        
        data = {}
        for x,title in enumerate(TITLES_COMMENT):
            respond = result[0][x]
            if type(respond) is datetime:
                respond = respond.strftime('%Y-%m-%d %H:%M:%S')
                
            data[title] = respond
        return data
    except Exception as e:
        return None

def createComment(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_COMMENT} (comment_id, commenter_username, publication_id, message, created_date) VALUES (
            "{data["comment_id"]}",
            "{data["commenter_username"]}",
            "{data["publication_id"]}",
            "{data["message"]}",
            "{data["created_date"]}")''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def deleteCommentFromDB(comment_id:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM {TABLE_COMMENT} WHERE comment_id = '{comment_id}' ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        return False
    
def likeComment(data:dict) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {RELATION_TABLE_RATE_COMMENT} (username, comment_id, rating) VALUES (
            "{data["username"]}",
            "{data["comment_id"]}",
            {data["rating"]})''')
        
        cursor.close()
        conn.commit()
        
        return True
    except Exception as e:
        return False
    
def getAllComment() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    cursor.execute(f'''SELECT * 
                   FROM {TABLE_COMMENT} 
                   ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()
    
def getAllRateComment() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    #cursor.execute(f'''SELECT SUM(CASE WHEN rating = 1 THEN 1 WHEN rating = 0 THEN -1 ELSE 0 END) 
    #               FROM {RELATION_TABLE_RATE_COMMENT}
    #               WHERE comment_id = 'cfa13586-f960-4418-816f-df74eb412ade' ''')
    
    cursor.execute(f'''SELECT *
                   FROM {RELATION_TABLE_RATE_COMMENT}
                   ''')
    result = cursor.fetchall()
    print(result)
    
    cursor.close()