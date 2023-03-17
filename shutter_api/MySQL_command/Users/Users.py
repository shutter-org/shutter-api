from shutter_api import MYSQL, IMAGEKIT
from shutter_api.MySQL_command.Tools import *
from shutter_api.MySQL_command.Gallerys import getGalleryPublications

def updateUser(username:str, newUsername:str=None, email:str=None, bio:str=None, picture:str=None, name:str=None) -> bool:
    try:
        if picture is not None:
            upload_response =  IMAGEKIT.upload(picture, file_name=username)
            if upload_response is None:
                return False
            picture = upload_response["url"]
            
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       UPDATE {TABLE_USER} u 
                       SET 
                       {f"""u.username = "{newUsername}" """ if newUsername is not None else ""}
                       {f"""{"," if newUsername is not None else ""}u.email = "{email}" """ if email is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None else ""}u.biography = "{bio}" """ if bio is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None else ""}u.profile_picture = "{picture}" """ if picture is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None or picture is not None else ""}u.name = "{name}" """ if name is not None else ""}
                       WHERE u.username = "{username}"; ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False

def deleteUserFromDB(userName:str) -> bool:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_USER} 
                       WHERE username = "{userName}";
                       ''')
        conn.commit()
        
        cursor.close()
        return True
    except Exception:
        return False
        
def getUserGallery(username:str, private:bool) -> list:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT g.gallery_id, g.title
                       FROM {TABLE_GALLERY} g
                       WHERE g.creator_username = "{username}" {f""" AND g.private = false""" if not private else ""}
                       ORDER BY g.created_date DESC
                       ''')
        result = cursor.fetchall()
        cursor.close()
        gallerys = []
        for x in result:
            data = {
                "gallery_id": x[0],
                "title":x[1],
                "publications":getGalleryPublications(x[0], username=username)
            }
            gallerys.append(data)
        
        
        return gallerys
    except Exception:
        return None
    
def getUserByUsername(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.username, u.biography, u.name, u.birthdate, u.profile_picture 
                       FROM {TABLE_USER} u 
                       WHERE username = "{username}"; 
                       ''')
        result = cursor.fetchall()[0]
        
        cursor.close()

        data = {
            "username": result[0],
            "biography":result[1],
            "name":result[2],
            "age":getAgeFromDate(result[3]),
            "profile_picture":result[4]
        }
    
        return data
    except Exception:
        return None
    
def getUserByUsernameDetail(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.username, u.email, u.biography, u.name, u.created_date, u.birthdate, u.profile_picture
                       FROM {TABLE_USER} u 
                       WHERE username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]
        
        cursor.close()

        data = {
            "username": row[0],
            "email":row[1],
            "biography":row[2],
            "name":row[3],
            "created_date": getIntervalOdTimeSinceCreation(row[4]),
            "birthdate":row[5].strftime('%Y-%m-%d'),
            "age":getAgeFromDate(row[5]),
            "profile_picture":row[6]
        }
    
        return data
    except Exception:
        return None
    
def getUserByUsernameLess(username:str) -> dict:
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.username, u.profile_picture 
                       FROM {TABLE_USER} u 
                       WHERE username = "{username}"; 
                       ''')
        result = cursor.fetchall()[0]
        
        cursor.close()
        data = {
            "username": result[0],
            "profile_picture":result[1]
        }
    
        return data
    except Exception:
        return None