---
title: JavaEE-Header
date: 2018-12-12 19:10:27
updated: 2018-12-21 23:49:16
categories: JavaEE
tags: [Header,request]
---

### docker+nginx(vue)获取真实ip

nginx必须安装`--with-http_realip_module`通过此命令`2>&1 nginx -V | tr -- - '\n' | grep http_realip_module`进行检查

`nginx -V` 可以查看到的编译参数和编译的模块(静态和动态)

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

经测试：

只需2，3设置即可，1设置无效，如果只设置1和3还是不是真实ip，所以变量`remote_addr`不是真实ip（该ip实际从哪里来待确定？），`X-Real-IP`是自定义header头，相当于key，要一致

### 总结

##### 方法一：

由于nginx安装在docker集群，nginx获取的ip（`remote_addr`）总是某个（不确定是哪里来的）的ip（10.255.0.3），因此1设置无效

解决nginx服务采用host模式，端口配置采用

```properties
    ports:
      - target: 8888
        published: 14881   #只有worker能访问该端口
        protocol: tcp
        mode: host  #版本要求3.2
```

采用了host就没了负载均衡了

##### 方法二：

是用客户端添加自定义头`X-Real-IP`但是前端请求暂时加不进去，且后端要修改获取ip的方法


参考

[在使用了NGINX的时候，如何获取访问用户的IP](https://www.imooc.com/article/19884)

[Unable to retrieve user's IP address in docker swarm mode](https://github.com/moby/moby/issues/25526)