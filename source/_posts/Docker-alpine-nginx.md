---
title: Docker-alpine-nginx
date: 2018-08-22 09:49:33
updated: 2018-11-06 11:20:19
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

### nginx常用调试

```sh
#查看ngixn是否启动
ps -ef|grep nginx
#查看错误日志,需要开启error_log /var/log/nginx/error.log warn;
cat /var/log/nginx/error.log
#重新加载配置
nginx -s reload
#重启nginx
nginx -s reopen
#停止nginx
nginx -s stop
#启动nginx
nginx
#测试配置文件语法问题
nginx -t
```

### nginx路径配置解释

```nginx
location /test {        
            root   /tmp/video;
        }
#用http://<url>/test/...访问的文件地址为/tmp/video/test
location /video {        
            root   /tmp/video;
        }
#用http://<url>/video/...访问的文件地址为/tmp/video/video
location / {        
            root   /tmp/video;
        }
#用http://<url>/...访问的文件地址为/tmp/video/
```

常用配置文件

```nginx
http {                                    
    include       mime.types;             
    default_type  application/octet-stream;
                                           
    #access_log  logs/access.log  main;    
                                           
    sendfile        on;                    
                                           
    keepalive_timeout  65;                 
                                           
    #gzip  on;                             
                                           
    server {                               
        listen       8888;             
        server_name  localhost;        
        location / {           
            root   /tmp/hikvision/video;
        }                               
    }                                   
                                        
} 
```



### nginx 代理

参考  [简明 Nginx Location Url 配置笔记](https://www.jianshu.com/p/e154c2ef002f)



* 正则匹配(`~`),URL包含`weather`都会走代理

  ```nginx
  location ~ /weather/ {
         proxy_pass  http://apicloud.mob.com;
      }
  ```

* 前缀匹配(`^~`),前缀是`/v1/weather/`开头的才走代理

  ```nginx
  location ^~ /v1/weather/ {
         proxy_pass  http://apicloud.mob.com;
      }
  ```

* 精确匹配(`=`),URL是`/demo` 多了少了都不行，才能进代理

  ```nginx
  location = /demo/ {
         proxy_pass  http://apicloud.mob.com;
      }
  ```
