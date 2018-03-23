---
title: Java-Springboot配置文件
date: 2018-03-22 13:07:49
updated: 2018-03-23 08:40:18
categories: Java
tags: [Java,springboot]
---

#### 配置文件

配置文件路径`resuources\application.properties`或者`resuources\application.yml`二者存一

1. `application.properties`与`application.yml`区别

   一个是树形目录，一个是单行配置。eg：`server.port=8080`等效于

   ```yaml
   server:
     port: 8080
   ```

2. 配置环境变量

   ```yaml
   diy:
     parmars: hello
   #配置文件引用say=hello
   say: ${diy.parmars}
   ```

   代码里面引用

   ```Java
    @Value("${diy.parmars}")
    private String imgUrl;
   ```

   ​

#### 常见配置

1. 数据库连接配置

   ```yaml
   spring:
     datasource:
        url: jdbc:mysql://10.14.0.1:3306/sqlname?useUnicode=true&characterEncoding=utf-8
        username: xxx
        password: xxxx
        driver-class-name: com.mysql.jdbc.Driver
   ```

2. springboot访问端口配置

   ```yaml
   server:
     port: 8080
   ```

3. 静态文件路径映射配置,如果配置了`spring.resources.static-location`会覆盖原来默认的静态文件设置`classpath:/META-INF/resources/,classpath:/resources/,classpath:/static/,classpath:/public/`，`file`路径指本地磁盘路径，window/Mac/linux的真实目录路径，例如window为`C:\\windos\\`

   ```yaml
   spring:
     resources:
        static-locations: <原来的静态文件配置>,file:/Users/xuanleung/Pictures/
   ```

   ​



#### 常见问题

1. springboot存储中文到mysql数据库乱码

   解决：在配置文件连接数据库地方添加`url: jdbc:mysql://<ip>:<端口>/<数据库名字>?useUnicode=true&characterEncoding=utf-8`

2. ​





#### 参考

[Springboot 之 静态资源路径配置](http://blog.csdn.net/zsl129/article/details/52906762)