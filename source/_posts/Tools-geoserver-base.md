---
title: Tools-geoserver-base
date: 2018-08-17 11:00:14
updated: 2018-08-20 16:45:21
categories: 工具
tags: [geoserver]
---

## 安装

镜像地址：[kartoza/geoserver:latest](https://github.com/kartoza/docker-geoserver)

环境要求：最小内存4g

`docker-compose.yml`

```yaml
version: '3'

services:
  geoserver:
    restart: always
    image: 	kartoza/geoserver:latest	
    ports:
      - "14018:8080"
    volumes:
      - "/dockerdata/v-geoserver/data:/opt/geoserver/data_dir"
    environment:
      - JAVA_OPTS= '-Xmx3072m' 
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == worker]
```

### 使用

1. 登陆

   访问http://192.168.204.182:14018/geoserver/web/使用[admin](geoserver)登陆

2. 创建工作区

   命名：xuan(自定义)

   命名空间URI：http://geoserver.org/xuan

   - [x] 默认工作区

3. 新建数据存储

   选`栅格数据源->ImagePyramid` 

   复制图层数据（该数据可以用Fwtools切图）到挂载目录`/dockerdata/v-geoserver/data`

   点击浏览找到数据目录，然后保存

4. 发布图层

   保存成功后，点击发布按钮

   默认设置，保存

5. 测试预览图层

   点击`Layer Preview` 选择图层进行预览



## 问题

1. geoserver添加图层预览时提示`java.lang.OutOfMemoryError: GC overhead limit exceeded`该错误

   解决把`-Xmx`设置更大，如果是虚拟机最小内存必须设置4g