---
title: SpringCould-config
date: 2018-04-18 23:14:52
updated: 2018-04-19 02:19:20
categories: Spring
tags: [SpringCould,config]
---

### 配置(config)中心

作用多服务统一配置管理，主要分配置中心服务端，和配置中心客户端（主要存储配置）

#### Config Server

1. 新建一个springboot项目，取名`configserver`，勾选

   - [x] Could discovery-> eureka server   注释掉了，引用了不注册报错，如果要用，就注册就行，这里是测试config所以先不注册
   - [x] Could config->config server

2. 在`application`启动类添加`@EnableConfigServer`

3. 新建一个git配置文件仓库，这里就在当前工程创建，因为这个反正都要上传git，在项目目录新建一个`config`目录,然后在目录里新建一个配置仓库`testrepo`,再在仓库添加配置文件`config-client-dev.properties`内容如下

   ```properties
   config-client.testsmsg = hello config me
   test = haa
   ```

4. 然后git commit  push推送到远程分支

5. 在配置文件`application.yml`添加如下内容

   ```yaml
   server:
     port: 8096
   spring:
     application:
       name: config-server
     cloud:
       config:
         label: master  #配置仓库分支
         server:
           git:
             uri: https://github.com/xuanfong1/SpringCould/   #配置仓库git地址
             search-paths: config/testrepo   #配置仓库路径
             username:   #访问git仓库的用户名，这里因为是开放项目所以不需要设置
             password:   #访问git仓库的密码
   ```

6. 访问http://127.0.0.1:8096/config-client/dev/master这个地址读取配置文件

   下面介绍http请求地址与资源文件映射问题

   Url :  /{application}/{profile}[/{label}]

   资源文件格式可以为

   - /{application}-{profile}.yml

   - /{label}/{application}-{profile}.yml

   - /{application}-{profile}.properties

   - /{label}/{application}-{profile}.properties

     举例：master分支有配置文件`config-client-dev.properties`访问的url为http://ip:port/config-client/dev/master

#### config client

1. 新建一个springboot项目，取名`configserver`，勾选

   - [ ] web->web
   - [ ] Could config->config client

2. 修改配置文件`application.properties`一定要修改为**`bootstrap.yml`**并添加如下内容

   ```yaml
   server:
     port: 8097
   spring:
     application:
       name: config-client
     cloud:
       config:
         label: master #指明远程仓库的分支
         profile: dev #dev(开放)、test(测试)、pro(正式)
         uri: http://127.0.0.1:8096/  #配置中心地址
   ```

3. 添加一个api接口

   ```
   @RestController
   public class HiController {
       @Value("${test}")  //调用配置中心的配置
       String test;

       @RequestMapping(value = "/hi")
       public String hi(){
           return test;
       }
   }
   ```

4. 访问http://127.0.0.1:8097/hi进行测试

