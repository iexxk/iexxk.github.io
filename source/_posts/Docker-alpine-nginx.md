---
title: Docker-alpine-nginx
date: 2018-08-22 09:49:33
updated: 2018-08-22 10:42:45
categories: Docker
tags: [Docker,nginx,alpine]

---

### alpine 安装nginx

```bash
apk update
#apk add nginx #安装
apk add nginx-mod-rtmp #安装带rtmp插件的nginx
ps aux | grep nginx #查看是否运行
vi /etc/nginx/nginx.conf #修改配置文件
```



#### 问题1 `nginx: [emerg] open() "/run/nginx/nginx.pid" failed (2: No such file or directory)`

解决：`mkdir /var/run/nginx`

#### 问题2 `nginx: [emerg] unknown directive "rtmp" in /etc/nginx/nginx.conf:16`

解决：在`/etc/nginx/nginx.conf`添加`include /etc/nginx/modules/*.conf;`

