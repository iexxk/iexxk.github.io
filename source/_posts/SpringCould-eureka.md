---
title: SpringCould-eureka
date: 2018-04-11 09:59:55
updated: 2018-04-11 21:58:31
categories: Spring
tags: [SpringBoot,SpringCould,eureka]
---

### eureka

[eureka](https://spring.io/guides/gs/service-registration-and-discovery/)是一个服务注册和发现模块

1. 新建springboot工程，作为eureka服务注册中心，勾选如下选项

   - [x]  Cloud Discovery->Eureka Server

2. 在`Application`类上添加注解`@EnableEurekaServer`声明注册中心

3. 在`Application.yml`配置文件添加内容：

   ```yaml
   server:
     port: 8091
   eureka:
     instance:
       hostname: 127.0.0.1 #指定该Eureka实例的主机名，本地默认127.0.0.1，部署docker时再试验
     client:
       register-with-eureka: false #Eureka默认也会作为客户端尝试注册，因此需禁用注册行为
       fetch-registry: false
   ```

4. 访问[127.0.0.1:8091](127.0.0.1:8091)可以进入管理页面查看注册了那些服务

5. 重复第一步，作为eureka客户端

6. 在`Application`类上添加注解`@EnableEurekaClient`声明客户端

7. 在`Application.yml`配置文件添加内容：

   ```yaml
   server:
     port: 8092
   spring:
     application:
       name: eureka-client
   eureka:
     client:
       service-url:
         defaultZone: http://127.0.0.1:8091/eureka/ #注意要加eureka，不然找不到
   ```

8. 再进入eureka服务注册中心就可以看到Application名为`eureka-client`的客户端

##### eureka高可用(未实践)

```yaml
spring:
  profiles: peer1                                 # 指定profile=peer1
server:
  port: 8761
eureka:
  instance:
    hostname: peer1                               # 指定当profile=peer1时，主机名
  client:
    serviceUrl:
      defaultZone: http://peer2:8762/eureka/      # 将自己注册到peer2这个Eureka上面去
###----------------第二个eureka注册中心互相注册即可-----------------------------------------  
spring:
  profiles: peer2
server:
  port: 8762
eureka:
  instance:
    hostname: peer2
  client:
    serviceUrl:
      defaultZone: http://peer1:8761/eureka/
###----------各个微服务端（客户的）只需修改成如下------------
defaultZone: http://peer1:8761/eureka/,http://peer2:8762/eureka
```







