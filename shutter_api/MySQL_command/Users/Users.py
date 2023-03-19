from shutter_api import MYSQL
from shutter_api.MySQL_command.Tools import *
from shutter_api.MySQL_command.Gallerys import getGalleryPublications


def getUsers(search:str) -> list or None:
    """
    get Users base on kyword

    Args:
        search (str): search keyword

    Returns:
        list or None: list of username, None if request fail
    """
    try:  
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        #TODO
        #ajout order by nb_follower
        ###################
        
        cursor.execute(f'''
                       SELECT u.username, u.profile_picture, u.name
                       FROM {TABLE_USER} u
                       WHERE u.username LIKE '{search}%'
                       LIMIT 10;
                       ''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        for row in result:
            data.append({
                "username": row[0],
                "profile_picture" : row[1],
                "name":row[2]
            })
        
        return data
    except Exception:
        return None
        

def updateUser(username:str, newUsername:str=None, email:str=None, bio:str=None, picture:str=None, name:str=None) -> bool:
    """
    update the username base on the param
    
    Args:
        username (str): current username
        newUsername (str, optional) : new username, default None.
        email (str, optional) : new email, default None.
        bio (str, optional) : new bio, default None.
        picture (base64, optional) : new picture in format of base64 or img link, default None.
        name (str, optional) : new name, default None.

    Returns:
        bool: if request succes
    """
    try:
        
            
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        if picture is not None:
            picture, file_id = addImgToKitioToUsers(picture,username)
        else:
            file_id = None
            
        if newUsername is not None:
            cursor.execute(f'''
                            SELECT u.profile_picture
                            FROM {TABLE_USER} u
                            WHERE u.username = "{username}";
                            ''')
            url = str(cursor.fetchall()[0][0])
            url = url.rsplit("?",1)[0]
            picture = updateUserImgToKitio(username, newUsername)

        cursor.execute(f'''
                       UPDATE {TABLE_USER} u 
                       SET 
                       {f"""u.username = "{newUsername}" """ if newUsername is not None else ""}
                       {f"""{"," if newUsername is not None else ""}u.email = "{email}" """ if email is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None else ""}u.biography = "{bio}" """ if bio is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None else ""}u.profile_picture = "{picture}" """ if picture is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None or picture is not None else ""}u.name = "{name}" """ if name is not None else ""}
                       {f""",u.file_id = "{file_id}" """ if file_id is not None else ""}
                       WHERE u.username = "{username}"; ''')
        conn.commit()
        
        cursor.close()
        return True
    except ValueError:
        return False

def deleteUserFromDB(username:str) -> bool:
    """
    Delete user from the data base

    Args:
        username (str): username

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
          
        cursor.execute(f'''
                       SELECT p.file_id
                       FROM {TABLE_PUBLICATION} p
                       WHERE p.poster_username = "{username}"
                       ''')
        files = [x[0] for x in cursor.fetchall()]
        cursor.execute(f'''
                       SELECT u.file_id
                       FROM {TABLE_USER} u
                       WHERE u.username = "{username}"
                       ''')
        files.append(cursor.fetchall()[0][0])
        
        
        cursor.execute(f'''
                       DELETE FROM {TABLE_USER} 
                       WHERE username = "{username}";
                       ''')
        
        deleteImageBulkFromImagekitio(files)
        conn.commit()
        
        cursor.close()
        return True
    except ValueError:
        return False
        
def getUserGallery(username:str, private:bool) -> list or None:
    """
    get the gallerys of a user

    Args:
        username (str): username
        private (bool): get the private gallerys

    Returns:
        list or None: list of gallery, None if request fail
    """
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
        for row in result:
            data = {
                "gallery_id": row[0],
                "title":row[1],
                "publications":getGalleryPublications(row[0], username=username)
            }
            gallerys.append(data)
        
        
        return gallerys
    except Exception:
        return None
    
def getUserByUsername(username:str) -> dict or None:
    """
    get a user data 

    Args:
        username (str): user username

    Returns:
        dict or None: None if request fail
            "username": str,
            "biography":str,
            "name":str,
            "age": int,
            "profile_picture": str,
            "created_date": str
            
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.username, u.biography, u.name, u.birthdate, u.profile_picture, u.created_date
                       FROM {TABLE_USER} u 
                       WHERE username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]
        
        cursor.close()

        data = {
            "username": row[0],
            "biography":row[1],
            "name":row[2],
            "age":getAgeFromDate(row[3]),
            "profile_picture":row[4],
            "created_date":getIntervalOdTimeSinceCreation(row[5])
        }
    
        return data
    except Exception:
        return None
    
def getUserByUsernameDetail(username:str) -> dict:
    """
    get a user data with more data

    Args:
        username (str): user username

    Returns:
        dict or None: None if request fail
            "username": str,
            "biography":str,
            "name":str,
            "age": int,
            "profile_picture": str,
            "created_date": str,
            "birthdate": str,
            "email": str
    """
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
    """
    get user with minimum data

    Args:
        username (str): user username

    Returns:
        dict or None: None if request fail
            "username": str,
            "profile_picture": str

    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()
        
        cursor.execute(f'''
                       SELECT u.username, u.profile_picture 
                       FROM {TABLE_USER} u 
                       WHERE username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]
        
        cursor.close()
        data = {
            "username": row[0],
            "profile_picture":row[1]
        }
    
        return data
    except Exception:
        return None