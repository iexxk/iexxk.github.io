---
title: JavaEE-Header
date: 2018-12-12 19:10:27
updated: 2018-12-12 19:16:47
categories: JavaEE
tags: [Header,request]
---





### docker+nginx(vue)获取真实ip

1. nginx设置代理

   ```nginx
   server {
       listen       8080;
       server_name  localhost;
   
       location / {
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           root   /usr/share/nginx/html;
           index  index.html index.htm;
       }
   }    
   ```

2. 代码设置

   ```java
       public RestResult login(@RequestBody User user,HttpServletRequest request) {
               String ip = request.getHeader("X-Real-IP");
               if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
                   ip = request.getHeader("X-Forwarded-For");
               }
               if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
                   ip = request.getHeader("Proxy-Client-IP");
               }
               if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
                   ip = request.getHeader("WL-Proxy-Client-IP");
               }
               if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
                   ip = request.getRemoteAddr();
               }
        }       
   ```

3. 请求头设置

   ```properties
   POST /app/index/login HTTP/1.1
   Host: 192.168.1.230:14083
   Content-Type: application/json
   X-Real-IP: 192.16.1.1
   cache-control: no-cache
   ```












参考

[在使用了NGINX的时候，如何获取访问用户的IP](https://www.imooc.com/article/19884)