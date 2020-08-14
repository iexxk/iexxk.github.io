---
title: Docker-make-ffmpeg-nginx
date: 2018-08-22 10:13:38
updated: 2020-08-06 10:00:55
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

![1534905867716](http://gt163.cn:14033/blog/20200806100035.png)

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





方式二:独立版(centos7)

资源准备

Nginx: [https://nginx.org/download/](https://nginx.org/download/)

Pure(rewrite模块): [https://ftp.pcre.org/pub/pcre/](https://ftp.pcre.org/pub/pcre/)

zlib(gzip模块): http://www.zlib.net/fossils/

openssl(ssl 功能):[https://www.openssl.org/source/](https://www.openssl.org/source/)

```bash
tar -zxvf nginx-1.15.12.tar.gz
tar -zxvf openssl-1.1.0l.tar.gz
tar -zxvf zlib-1.2.11.tar.gz
tar -zxvf pcre-8.43.tar.gz  

cd pcre-8.43/
./configure 
make && make install

cd ../zlib-1.2.11/
./configure 
make && make install

cd ../openssl-1.1.0l/
./config
make && make install

cd ../nginx-1.15.12/
./configure --prefix=/usr/local/nginx --with-pcre=../pcre-8.43 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.1.0l --add-module=../nginx-rtmp-module-1.2.1  
make && make install
```

安装ffpmeg

```shell
#安装epel包
yum install -y epel-release 
#导入签名
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
#导入签名
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro 
#升级软件包
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
#更新软件包
yum update -y
#安装ffmpeg
yum install -y ffmpeg
#检查版本
ffmpeg -version
```

配置测试

nginx配置vim /usr/local/nginx/conf/nginx.conf

```nginx
user root;
worker_processes 1;
events {
	worker_connections 1024;
}
# rtmp流
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
# hls流
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       8888;
        server_name  localhost;
        location / {
            root   /tmp/hikvision/video;
        }
        location /hls {
           types {
             application/vnd.apple.mpegurl m3u8;
             video/mp2t ts;
           }
           root /tmp;
           add_header Cache-Control no-cache;
        }
    }
}
```

测试

```bash
#本地视频测试rtmp://10.30.11.150:1935/myapp/test1
ffmpeg -re -i "/root/nginxbuild/test.mp4" -vcodec libx264 -vprofile baseline -acodec aac  -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 rtmp://10.30.11.150:1935/myapp/test1
#rtmp视频测试rtmp://10.30.11.150:1935/myapp/video1
ffmpeg -rtsp_transport tcp -i rtsp://admin:admin@10.30.11.119:554/h264/ch1/main/av_stream  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 704x576 -q 10 -f flv rtmp://10.30.11.150:1935/myapp/video1
ffmpeg -i rtsp://admin:admin@10.30.11.119:554/h264/ch1/main/av_stream -tune zerolatency -vcodec libx264 -preset ultrafast -b:v 400k -s 720x576 -r 25 -acodec libfaac -b:a 64k -f flv rtmp://10.30.11.150:1935/myapp/video1
#hls测试http://10.30.11.150:8888/hls/video1.m3u8
ffmpeg -rtsp_transport tcp -i rtsp://admin:admin@10.30.11.119:554/h264/ch1/sub/av_stream  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 704x576 -q 10 -f flv rtmp://10.30.11.150:1935/hls/video1
```



### supervisor多服务

[supervisor](https://docs.docker.com/config/containers/multi-service_container/)

[Alpine Linux Repository本地镜像制作 v2](https://my.oschina.net/funwun/blog/710877)

[centos7+nginx+rtmp+ffmpeg搭建流媒体服务器](https://www.jianshu.com/p/aa7f9e204a62)