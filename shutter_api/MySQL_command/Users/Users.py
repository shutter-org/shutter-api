import struct

from shutter_api import MYSQL
from shutter_api.Keys import SQL_ENCRYPTION_KEY
from shutter_api.MySQL_command.Galleries import getGalleryPublications
from shutter_api.Tools import *


def getUsers(search: str) -> list or None:
    """
    get Users base on keyword

    Args:
        search (str): search keyword

    Returns:
        list or None: list of username, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT u.username, u.profile_picture, u.name
                       FROM {TABLE_USER} u
                       WHERE u.username LIKE "{search}%"
                       OR u.name LIKE "{search}%"
                       LIMIT 12;
                       ''')
        result = cursor.fetchall()
        cursor.close()
        data = []
        for row in result:
            data.append({
                "username": row[0],
                "profile_picture": row[1],
                "name": row[2]
            })

        return data
    except Exception:
        return None


def updateUser(username: str, newUsername: str = None, email: str = None, bio: str = None, picture: str = None,
               name: str = None, password: str = None) -> bool:
    """
    update the username base on the param
    
    Args:
        username (str): current username
        newUsername (str, optional) : new username, default None.
        email (str, optional) : new email, default None.
        bio (str, optional) : new bio, default None.
        picture (base64, optional) : new picture in format of base64 or img link, default None.
        name (str, optional) : new name, default None.
        password (str, optional) : new password, default None.

    Returns:
        bool: if request succes
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        if picture is not None:
            picture, file_id = addImgToKitioToUsers(picture, username)
        else:
            file_id = None

        if newUsername is not None:
            cursor.execute(f'''
                            SELECT u.profile_picture
                            FROM {TABLE_USER} u
                            WHERE BINARY u.username = "{username}";
                            ''')
            url = str(cursor.fetchall()[0][0])
            url = url.rsplit("?", 1)[0]
            picture = updateUserImgToKitio(username, newUsername)

        if password:
            password = encrypt(password, SQL_ENCRYPTION_KEY)

        cursor.execute(f'''
                       UPDATE {TABLE_USER} u 
                       SET 
                       {f"""u.username = "{newUsername}" """ if newUsername is not None else ""}
                       {f"""{"," if newUsername is not None else ""}u.email = "{email}" """ if email is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None else ""}u.biography = "{bio}" """ if bio is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None else ""}u.profile_picture = "{picture}" """ if picture is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None or picture is not None else ""}u.name = "{name}" """ if name is not None else ""}
                       {f""",u.file_id = "{file_id}" """ if file_id is not None else ""}
                       {f"""{"," if newUsername is not None or email is not None or bio is not None or picture is not None or name is not None else ""}u.password = "{password}" """ if password is not None else ""}
                       WHERE BINARY u.username = "{username}"; 
                       ''')
        conn.commit()

        cursor.close()
        return True
    except ValueError:
        return False


def deleteUserFromDB(username: str) -> bool:
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
                       WHERE BINARY p.poster_username = "{username}"
                       ''')
        files = [x[0] for x in cursor.fetchall()]
        cursor.execute(f'''
                       SELECT u.file_id
                       FROM {TABLE_USER} u
                       WHERE BINARY u.username = "{username}"
                       ''')
        files.append(cursor.fetchall()[0][0])

        cursor.execute(f'''
                       DELETE FROM {TABLE_USER} 
                       WHERE BINARY username = "{username}";
                       ''')

        deleteImageBulkFromImagekitio(files)
        conn.commit()

        cursor.close()
        return True
    except ValueError:
        return False


def getUserGallery(username: str, private: bool) -> list or None:
    """
    get the galleries of a user

    Args:
        username (str): username
        private (bool): get the private galleries

    Returns:
        list or None: list of gallery, None if request fail
    """
    try:
        conn = MYSQL.get_db()
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT g.gallery_id, g.title, g.private
                       FROM {TABLE_GALLERY} g
                       WHERE BINARY g.creator_username = "{username}" {f""" AND g.private = false""" if not private else ""}
                       ORDER BY g.created_date DESC
                       ''')
        result = cursor.fetchall()
        cursor.close()
        galleries = []
        for row in result:
            data = {
                "gallery_id": row[0],
                "title": row[1],
                "publications": getGalleryPublications(row[0], username=username),
                "private": struct.unpack('?', row[2])[0]
            }
            galleries.append(data)

        return galleries
    except Exception:
        return None


def getUserByUsername(username: str) -> dict or None:
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
                       WHERE BINARY username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]

        cursor.close()

        data = {
            "username": row[0],
            "biography": row[1],
            "name": row[2],
            "age": getAgeFromDate(row[3]),
            "profile_picture": row[4],
            "created_date": getIntervalOdTimeSinceCreation(row[5])
        }

        return data
    except Exception:
        return None


def getUserByUsernameDetail(username: str) -> dict:
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
                       WHERE BINARY username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]

        cursor.close()

        data = {
            "username": row[0],
            "email": row[1],
            "biography": row[2],
            "name": row[3],
            "created_date": getIntervalOdTimeSinceCreation(row[4]),
            "birthdate": row[5].strftime('%Y-%m-%d'),
            "age": getAgeFromDate(row[5]),
            "profile_picture": row[6]
        }

        return data
    except Exception:
        return None


def getUserByUsernameLess(username: str) -> dict:
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
                       WHERE BINARY username = "{username}"; 
                       ''')
        row = cursor.fetchall()[0]

        cursor.close()
        data = {
            "username": row[0],
            "profile_picture": row[1]
        }

        return data
    except Exception:
        return None
