import os
import time
import uuid
import sys
import requests
from minio import Minio
from minio.error import ResponseError
import warnings

warnings.filterwarnings('ignore')
images = sys.argv[1:]
minioClient = Minio("gt163.cn:14033",
                    access_key='root', secret_key='password', secure=False)
result = "Upload Success:\n"
date = time.strftime("%Y%m%d%H%M%S", time.localtime())

for image in images:
    file_type = os.path.splitext(image)[-1]
    new_file_name = date + file_type
    if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".gif"):
         content_type ="image/"+file_type.replace(".", "");
    else:
        content_type ="image/jpg"
        continue
    try:
        minioClient.fput_object(bucket_name='blog', object_name= new_file_name, file_path=image,content_type=content_type)
        if image.endswith("temp"):
            os.remove(image)
        result = result +"http://gt163.cn:14033" + "/blog/"  + new_file_name + "\n"
    except ResponseError as err:
        result = result + "error:" + err.message + "\n"

print(result)