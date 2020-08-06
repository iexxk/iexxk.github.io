---
title: minio搭建图床
date: 2020-08-05 18:11:05
updated: 2020-08-05 18:27:10
categories: 杂谈
tags: [图床,minio,oss]
---

### minio搭建图床

minio部署见docker脚本



### 图床客户端工具

#### 方案一：typora+python+minio(采用)

##### 安装

```shell
git clone https://github.com/minio/minio-py
cd minio-py
#需要代理下载
sudo python setup.py install
```

##### 脚本

```python
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
minioClient = Minio("ip:port",
                    access_key='用户名', secret_key='密码', secure=False)
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
        result = result +"http://ip:port" + "/blog/"  + new_file_name + "\n"
    except ResponseError as err:
        result = result + "error:" + err.message + "\n"
print(result)
```

参考

[Minio+Nginx搭建私有图床，写博客从未这么爽](https://zhuanlan.zhihu.com/p/139529477)

[python-client-quickstart-guide](https://docs.min.io/docs/python-client-quickstart-guide.html)

#### 方案二：upic+typora+minio

参考：[Typora搭配uPic使用minIO自建图床](https://www.hfge.net/privatecloud/typora-minio.html)

### 注意事项

minio图片不能预览

1. 需要设置

![image-20200805182053298](http://gt163.cn:14033/blog/20200805182056.png)

2. 以及上传图片需要设置content_type为`image/jpg`

