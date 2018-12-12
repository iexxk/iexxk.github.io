---
title: Docker-make-ffmpeg-nginx
date: 2018-08-22 10:13:38
updated: 2018-08-22 10:13:38
categories: Docker
tags: [Docker,nginx,ffmpeg]
---

## 准备工作

#### 手动安装

```bash
apk update
#安装ngix 和 ffmpeg
apk add nginx-mod-rtmp ffmpeg
#创建目录解决pid错误问题
mkdir /var/run/nginx
#启动nginx
nginx
#使用ffmpeg进行转流
ffmpeg -rtsp_transport tcp -i rtsp://admin:12345@192.168.1.193:554  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 -f flv rtmp://127.0.0.1:1935/hls/video1
```

```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes 1;
#error_log /var/log/nginx/error.log warn;
# 包含插件rtmp
include /etc/nginx/modules/*.conf;
events {
	worker_connections 1024;
}
rtmp {    
        server {    
            listen 1935;    
        
            application myapp {    
                live on;    
            }    
            application hls {    
                live on;    
                hls on;    
                hls_path /tmp/hls;    
        				hls_fragment 1s;     
       	        hls_playlist_length 3s;   
	 				 }    
        }    
} 
```

成功输出：

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/1534905867716.png)



### dockerfile编写

方式一:集成版

```dockerfile
# 生成镜像name:tomcat:8-alpine-ffmpeg
FROM tomcat:8-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /conf/supervisord.conf

RUN  apk add --no-cache tzdata nginx-mod-rtmp ffmpeg supervisor \
	&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && mkdir -p /var/run/nginx 
ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-c", "/conf/supervisord.conf"] 
```



#### 解决nginx重启端口占用

修改`supervisord.conf`中的`command= nginx`为

`command= nginx -g "daemon off;"`



##### supervisord.conf

```properties
[supervisord]
; 启动到前端, 用于docker
nodaemon=true
; 设置pid文件路径
pidfile=/var/run/supervisord.pid

; 配置nginx
[program:nginx]
; 配置日志输出到控制台, 用于docker收集日志
stdout_logfile=/dev/stdout
; 去掉日志rotation
stdout_logfile_maxbytes=0
autorestart=true
priority=900
command= nginx

; 配置ffmpeg
[program:ffmpeg]
; 配置日志输出到控制台, 用于docker收集日志
stdout_logfile=/dev/stdout
; 去掉日志rotation
stdout_logfile_maxbytes=0
autorestart=true
priority=800
command=ffmpeg -rtsp_transport tcp -i rtsp://admin:12345@192.168.1.193:554  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 -f flv rtmp://127.0.0.1:1935/hls/video1

; 配置tomcat
[program:tomcat]
; 配置日志输出到控制台, 用于docker收集日志
stdout_logfile=/dev/stdout
; 去掉日志rotation
stdout_logfile_maxbytes=0
autorestart=true
priority=700
command=catalina.sh run
```



##### nginx.conf

```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes 1;
#error_log /var/log/nginx/error.log warn;
# 包含插件rtmp
include /etc/nginx/modules/*.conf;
events {
	worker_connections 1024;
}
rtmp {    
        server {    
            listen 1935;    
        
            application myapp {    
                live on;    
            }    
            application hls {    
                live on;    
                hls on;    
                hls_path /tmp/hls;    
        				hls_fragment 1s;     
       	        hls_playlist_length 3s;   
	 				 }    
        }    
} 
```



##### 应用

```dockerfile
#基础镜像选择alpine 小巧安全流行方便
FROM tomcat:8-alpine-ffmpeg
#复制固定路径下打包好的jar包(target/*.jar)并重命名到容器跟目录(/app.jar)，或ADD
COPY target/hikvision.war /usr/local/tomcat/webapps/
#覆写配置
COPY supervisord.conf /conf/supervisord.conf

#健康检查 -s 静默模式，不下载文件
#HEALTHCHECK CMD wget -s http://127.0.0.1:14030/actuator/health || exit 1
#启动容器执行的命令 java -jar app.jar ,如果加其他参数加 ,"-参数",
# 不需要该命令通过镜像上层的supervisor进行控制
#CMD ["catalina.sh", "run"]
```

##### 部署

```yaml
  hikvision:
    restart: always
    image: manage/test/ygl/hikvision:latest
    volumes:
      - /logs/ygl-hikvision:/app/log
    ports:
      - 14085:8080
      - 14086:1935
```

##### 测试

使用vle media player进行网络串流播放`rtmp://192.168.1.230:14086/hls/video1`





方式二:独立版

```dockerfile

```





### supervisor多服务

[supervisor](https://docs.docker.com/config/containers/multi-service_container/)

[Alpine Linux Repository本地镜像制作 v2](https://my.oschina.net/funwun/blog/710877)