from shutter_api import *
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio.models.RenameFileRequestOptions import RenameFileRequestOptions
import random

def addImgToKitioToUsers(img, name:str) -> tuple:
    """
    This function upload a image to kitio in the user File

    Args:
        img (base64): imgBytes
        name (str): name of the ima

    Returns:
        str: url
        str: file_id
    """
    options = UploadFileRequestOptions(use_unique_file_name=False,overwrite_file=True, folder="users")
    upload_response =  IMAGEKIT.upload_file(file=img, file_name=name,options=options)
    url = f"{upload_response.url}?{int(random.random()*100000000000)}"
    return url , upload_response.file_id

def addImgToKitioToPublications(img, publication_id:str) -> tuple:
    """
    This function upload a image to kitio in the publications file

    Args:
        img (base64): imgBytes
        publication_id (str): name of the ima

    Returns:
        str: url
        str: file_id
    """
    options = UploadFileRequestOptions(use_unique_file_name=False,overwrite_file=True, folder="publications")
    upload_response =  IMAGEKIT.upload_file(file=img, file_name=publication_id,options=options)
    url = f"{upload_response.url}?{int(random.random()*100000000000)}"
    return url , upload_response.file_id

def deleteImageFromImagekiTio(file_id:str) -> None:
    IMAGEKIT.delete_file(file_id=file_id)


def updateUserImgToKitio(oldName:str, newName:str) -> str:
    """
    This function update the name of the old Username in imagekit.io for the new one

    Args:
        oldName (str): old username
        newName (str): new username

    Returns:
        str: new Url
    """
    oldUrl = f"/users/{oldName}"
    newUrl = f"{newName}"
    options = RenameFileRequestOptions(file_path=oldUrl, new_file_name=newUrl)
    IMAGEKIT.rename_file(options=options)
    return f"{IMAGE_URL_ENDPOINT}{newUrl}?{int(random.random()*100000000000)}"
    