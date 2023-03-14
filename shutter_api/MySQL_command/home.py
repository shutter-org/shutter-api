from shutter_api import MYSQL
from .tableName import *


def command() -> None:
    conn = MYSQL.get_db()
    cursor = conn.cursor()
    
    print("ok")
    cursor.execute(f'''
                   
                   ''')
    
    cursor.close()
    conn.commit()
    print("executed")