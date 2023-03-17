from shutter_api import MYSQL
from .Tools import *

def createNewUser(data:dict) -> bool:
    
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_USER} (username, password, email, name, created_date, birthdate, profile_picture) VALUES (
            "{data["username"]}",
            "{data["password"]}",
            "{data["email"]}",
            "{data["name"]}",
            "{data["created_date"]}",
            "{data["birthdate"]}",
            "{"https://imgs.search.brave.com/ZGS8dDvM1Atr05xVh0iH_Lk8XULxvAZ2vP5CV1u-u8s/rs:fit:474:225:1/g:ce/aHR0cHM6Ly90c2Uy/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC55/dGU3clJuYkNuV2kx/Z2lyaXdUT3Z3SGFI/YSZwaWQ9QXBp"}")''')
        cursor.close()
        conn.commit()
        
        return True
    except Exception:
        return False
    
