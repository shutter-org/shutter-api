from shutter_api import *
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


def addImgToKitio(img, name:str) -> str:
    upload_response =  IMAGEKIT.upload_file(file=img, file_name=name,options=UploadFileRequestOptions(use_unique_file_name=False))
    url = IMAGE_URL_ENDPOINT + upload_response.file_path
    return url
    