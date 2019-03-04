---
title: nginx常用配置总结
date: 2019-01-29 23:21:37
updated: 2019-03-02 17:02:33
categories: Tools
tags: [nginx]
---

## 多二级/三级域名多服务nginx配置

常用命令

```bash
#启动
/usr/local/nginx/sbin/nginx
#停止
/usr/local/nginx/sbin/nginx -s stop
#检查脚本
/usr/local/nginx/sbin/nginx -t
#重新加载配置
/usr/local/nginx/sbin/nginx -s reload
```

`nginx.conf`

```nginx
#指定nginx 用户 组
#user sure sure;
#内容存进程的id，作用防止多个进程启动
pid    /usr/local/nginx/conf/nginx.pid;
#错误日志（从左到右：debug最详细 crit最少）
#[ debug | info | notice | warn | error | crit ] 
error_log  /usr/local/nginx/logs/error.log crit;

#启动进程,通常设置成和cpu的数量相等，或者设置auto
worker_processes 24;
#在linux 2.6内核下开启文件打开数为65535
worker_rlimit_nofile 65535;

events {
    #Epoll: 使用于Linux内核2.6版本及以后的系统
    use epoll;
    #所以nginx支持的总连接数就等于worker_processes * worker_connections
    worker_connections 65535;
}

http {
    #文件扩展名与类型对应关系
    include mime.types;
    #没有找到对应类型使用application/octet-stream
    default_type application/octet-stream;

    #访问日志关
    access_log off;
    # 隐藏nginx版本，防止通过版本漏洞攻击
    server_tokens off;
    
    server_names_hash_bucket_size 128;
    client_header_buffer_size 32k;
    large_client_header_buffers 4 32k;

    sendfile on;
    tcp_nopush on;
    #连接超时时间
    keepalive_timeout 120;
    tcp_nodelay on;

    gzip on;
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_vary on;

    #解决iframe跨域问题
    add_header P3P "CP=CAO PSA OUR";

    #解决页面部分缓存问题
    ssi on;
    ssi_silent_errors on;
    ssi_types text/shtml;
    ssi_types text/action;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" $http_x_forwarded_for';
    log_format mlnormal '$remote_addr|$remote_user|[$time_local]|$host|"$request"|'
                        '$status|$body_bytes_sent|"$http_referer"|'
                        '"$http_user_agent"|$http_x_forwarded_for|'
                        '$upstream_addr|$upstream_status|$upstream_response_time|'
                        '$server_addr';
    include vhost/*.conf;
}

```

子配置目录`vhost/*.conf`,支持多个域名对应服务的配置文件，一个服务对应一个二级域名文件

```nginx

#均衡代理，以及模式设置
upstream webcs {
    # 过源IP进行HASH的机制。可以解决session问题
    ip_hash;
    #tomcat服务的访问地址
    server 134.175.14.8:8042 max_fails=2 fail_timeout=30s;
    server 134.175.151.120:8043 max_fails=2 fail_timeout=30s;
}

server {
    listen 80;
    #listen 443 ssl;
    #域名访问地址
    # 多个域名 server_name ... iexxk.com www.iexxk.com;
    server_name    outtest.iexxk.com;
    index  index.htm index.html index.jsp;
    #tomcat webapp目录，或这dobase目录
    root   /data/web/webcs;

    #ssl_certificate /data/ssl/shenqi.cer;
    #ssl_certificate_key /data/ssl/shenqi.key;
    #ssl_session_timeout 5m;

    access_log /usr/local/nginx_logs/login.access.log mlnormal;

    location ~ ^/WEB-INF/* {
        deny all;
    }

    location ~ .(svn|git|cvs) {
        deny all;
    }

    location ~.*\.(jsp|do|shtml)?$ {
        #proxy_pass配置为：http:// + upstream策略名称
        proxy_pass        http://webcs;
        proxy_next_upstream http_500 http_502 http_503 http_504 error timeout invalid_header;
        proxy_redirect    off;
        proxy_set_header  Host $host;
        proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header  X-Real-IP  $remote_addr;
        #include /usr/local/nginx/conf/proxy.conf;
    }

    location ~* \.(gif|jpg|jpeg|png|bmp|swf|js|css)$ {
        expires 30d;
    }
}
```

### 配置ssl/https

```nginx
upstream res {
    ip_hash;
    server 172.16.16.8:14081 max_fails=2 fail_timeout=30s;
    server 172.16.16.8:14081 max_fails=2 fail_timeout=30s;
}

server {
    listen 80;
    listen 443 ssl;
    server_name    outtest.res.suresvip.com;

#证书相关配置
    ssl  on;  #注意这个用on其他所有改nginx配置的网站都会重定向到https,所以改用off不会影响其他的，但是不会自动重定向
    ssl_certificate /usr/local/nginx/ssl/1_outtest.res.suresvip.com_bundle.crt;
    ssl_certificate_key /usr/local/nginx/ssl/2_outtest.res.suresvip.com.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2; #按照这个协议配置
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

#注释下面的不然使用https访问会下载文件
#    index  index.htm index.html index.jsp;
#    root   /data/web/res1;

    access_log /usr/local/nginx_logs/login.access.log mlnormal;

    location ~ ^/WEB-INF/* {
        deny all;
    }

    location ~ .(svn|git|cvs) {
        deny all;
    }

    location ~.* {
        proxy_pass        http://res;
        proxy_next_upstream http_500 http_502 http_503 http_504 error timeout invalid_header;
        proxy_redirect    off;
        proxy_set_header  Host $host;
        proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header  X-Real-IP  $remote_addr;
        #include /usr/local/nginx/conf/proxy.conf;
    }

    location ~* \.(gif|jpg|jpeg|png|bmp|swf|js|css)$ {
        expires 30d;
    }
}

```



