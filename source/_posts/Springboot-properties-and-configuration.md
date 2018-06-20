---
title: Springboot配置文件
date: 2018-03-22 13:07:49
updated: 2018-06-20 09:28:04
categories: Spring
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
    private String imgUrl;​
   ```


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

4. 文件上传大小限制(-1不限制)（128KB）

   ```yaml
   spring: 
     servlet:
       multipart:
         max-file-size: -1
         max-request-size: -1
   ```


#### `application.yml`与`bootstrap.yml`区别

加载顺序`bootstrap.yml `->`application.yml`

`bootstrap.yml`常用于一些系统级别参数，不被更改

`application.yml` 应用级别，可以被更改，通过config service服务

`bootstrap.yml`常用于应用程序引导阶段例如

* spring config server配置
* application.name配置

使用config server时，`bootstrap.yml`常用配置

```yaml
spring:
  application:
    name: service-a
  cloud:
    config:
      uri: http://127.0.0.1:8888
      fail-fast: true
      username: user
      password: ${CONFIG_SERVER_PASSWORD:password}
      retry:
        initial-interval: 2000
        max-interval: 10000
        multiplier: 2
        max-attempts: 10
```

在不考虑加载顺序，两个配置是可以通用的





#### 常见问题

1. springboot存储中文到mysql数据库乱码

   解决：在配置文件连接数据库地方添加`url: jdbc:mysql://<ip>:<端口>/<数据库名字>?useUnicode=true&characterEncoding=utf-8`

2. `application.yml`添加注释报错，提示找不到`Failed to load property source from location 'classpath:/application.yml'`

   解决：检查文件编码格式，不是`utf-8`修改为`utf-8`





#### 参考

[Springboot 之 静态资源路径配置](http://blog.csdn.net/zsl129/article/details/52906762)