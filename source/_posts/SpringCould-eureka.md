---
title: SpringCould-eureka
date: 2018-04-11 09:59:55
updated: 2018-07-25 13:53:02
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
#多节点固定模式,文件名application-peer1.yml
spring:
  application:
    name: ${APPLICATION_NAME:eureka-center}
server:
  port: ${EUREKA_PORT:14031}
eureka:
  instance:
    hostname: ${EUREKA_HOST:eureka-center-peer1}  #指定该Eureka实例的主机名，需要host映射
    prefer-ip-address: false
  client:
    serviceUrl:  #高可用
      defaultZone:  ${EUREKA_CENTER_REG:http://eureka-center-peer2:14032/eureka/}
###----------------第二个eureka注册中心互相注册即可-----------------------------------------  
#多节点固定模式,文件名application-peer2.yml
spring:
  application:
    name: ${APPLICATION_NAME:eureka-center}
server:
  port: ${EUREKA_PORT:14032}
eureka:
  instance:
    hostname: ${EUREKA_HOST:eureka-center-peer2}  #指定该Eureka实例的主机名，需要host映射
    prefer-ip-address: false
  client:
    serviceUrl:  #高可用
      defaultZone:  ${EUREKA_CENTER_REG:http://eureka-center-peer1:14031/eureka/}
```

启动:

`java -jar app.jar --spring.profiles.active=peer1`

`java -jar app.jar --spring.profiles.active=peer2`

注意：

1. 高可用启动，application.name一定要一致
2. 一定要指定端口号
3. 不能禁用自我注册，注意配置文件加载顺序及覆盖顺序

### [健康检查](https://spring.io/guides/gs/actuator-service/)

```groovy
   compile('org.springframework.cloud:spring-cloud-starter-netflix-eureka-server')
  //上面的包包含下面的依赖,因此springcould不需要添加该依赖
 compile("org.springframework.boot:spring-boot-starter-actuator")
```

常用链接

```
$ curl localhost:8080/actuator/health
{"status":"UP"}
$ curl localhost:8080/actuator
{"_links":{"self":{"href":"http://127.0.0.1:14031/actuator","templated":false},"health":{"href":"http://127.0.0.1:14031/actuator/health","templated":false},"info":{"href":"http://127.0.0.1:14031/actuator/info","templated":false}}}
```

dockerfile

```
HEALTHCHECK  --interval=5m --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:14031/actuator/health || exit 1
 # --quiet  安静模式
 # --tries=1  重试次数
 # --spider  不下载任何资料
 
 wget --quiet --tries=1 --spider http://127.0.0.1:14031/actuator/health
  
```



[Wget命令参数及使用](http://blog.51cto.com/snaile/1600281)





问题：

```
EMERGENCY! EUREKA MAY BE INCORRECTLY CLAIMING INSTANCES ARE UP WHEN THEY'RE NOT. RENEWALS ARE LESSER THAN THRESHOLD AND HENCE THE INSTANCES ARE NOT BEING EXPIRED JUST TO BE SAFE.
```

原因据说是

注册中心不是高可用的原因

出处：https://www.cnblogs.com/xiaojf/p/7919088.html



