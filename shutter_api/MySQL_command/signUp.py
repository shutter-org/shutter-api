from shutter_api import MYSQL
from .Tools import *
from shutter_api.Keys import ENCRYPTION_KEY, SQL_ENCRYPTION_KEY
URL = "https://imgs.search.brave.com/ZGS8dDvM1Atr05xVh0iH_Lk8XULxvAZ2vP5CV1u-u8s/rs:fit:474:225:1/g:ce/aHR0cHM6Ly90c2Uy/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC55/dGU3clJuYkNuV2kx/Z2lyaXdUT3Z3SGFI/YSZwaWQ9QXBp"
def createNewUser(data:dict) -> bool:
    """
    MySQL request to create a new user

    Args:
        data (dict):
            "username": str
            "password": str
            "email":str
            "name": str
            "created_date: str
            "birthdate": str

    Returns:
        bool: if request succes
    """
    password = encrypt(decrypt(data["password"], ENCRYPTION_KEY), SQL_ENCRYPTION_KEY)
    try:
        pictureURL, file_id = addImgToKitioToUsers(URL, data["username"])
        
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''INSERT INTO {TABLE_USER} (username, password, email, name, created_date, birthdate, profile_picture, file_id) VALUES (
            "{data["username"]}",
            "{password}",
            "{data["email"]}",
            "{data["name"]}",
            "{data["created_date"]}",
            "{data["birthdate"]}",
            "{pictureURL}",
            "{file_id}")
            ''')
        cursor.close()
        conn.commit()
        
        return True
    except ValueError:
        return False
    
