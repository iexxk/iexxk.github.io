---
title: Docker-Disk-Space-Full
date: 2018-08-27 16:47:51
updated: 2018-08-27 16:47:51
categories: Docker
tags: [Docker,Disk]
---

## docker占用大量磁盘空间分析

#### linux 磁盘分析

`df -h` 查看挂载使用情况

` du -h --max-depth=1 /var/lib/docker/overlay2` 查看某个目录下文件夹大小

#### docker 磁盘空间占用情况

查看docker 空间分布

```bash
[root@environment-test1 ~]# docker system df
TYPE              TOTAL      ACTIVE       SIZE             RECLAIMABLE
Images            26         6            4.554GB          2.513GB (55%)
Containers        8          6            157.7GB          157.3GB (99%)
Local Volumes     0          0            0B               0B
Build Cache       0          0            0B               0B
```

查看空间占用细节`docker system df -v`会显示

```
[root@environment-test1 ~]# docker system df -v
Images space usage:

REPOSITORY                               TAG                 IMAGE ID            CREATED ago         SIZE                SHARED SIZE         UNIQUE SiZE         CONTAINERS
redis                                    latest              4e8db158f18d        3 weeks ago ago     83.4MB              58.6MB              24.8MB              2

Containers space usage:

CONTAINER ID        IMAGE                              COMMAND                  LOCAL VOLUMES       SIZE                CREATED ago          STATUS                        NAMES                   
2f9172a5f6d2        manage/test/ygl/hikvision:latest   "/usr/bin/supervisor…"   0                   157GB               42 hours ago ago     Dead                          manager-test-ygl_hikvision.1.6deoeddsuari0ob63cddg8f28
3bd29db83e99        redis:latest                       "docker-entrypoint.s…"   0                   0B                  42 hours ago ago     Exited (137) 16 minutes ago   manager-test-ygl_redis.1.ha792r91z4erzmn967sf9u4zx

Local Volumes space usage:

VOLUME NAME         LINKS               SIZE

Build cache usage: 0B
```

最后找到占用最多的容器，分析原因解决即可