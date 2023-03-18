from shutter_api import *
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import random


def addImgToKitio(img, name:str) -> str:
    options = UploadFileRequestOptions(use_unique_file_name=False,overwrite_file=True)
    upload_response =  IMAGEKIT.upload_file(file=img, file_name=name,options=options)
    url = IMAGE_URL_ENDPOINT + upload_response.file_path + f"?{int(random.random()*100000000000)}"
    return url
    