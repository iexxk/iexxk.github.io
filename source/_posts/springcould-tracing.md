---
title: SpringCould-Tracing
date: 2018-04-22 22:08:49
updated: 2021-04-02 17:24:30
categories: Spring
tags: [SpringCould,Tracing,Sleuth]
---

## 方式一docker-zipkin+zipkin+sleuth

请求原理图

```mermaid
graph LR
请求-->微服务客户端-->sleuth采集请求-->zipkin发送请求的信息-->docker-zipkin接受并展示
```

##### sleuth 采样+++zipkin 发送分析展示采样数据

1. 安装[penzipkin/docker-zipkin](https://github.com/openzipkin/docker-zipkin) 服务端，听说官方不建议编译，直接提供jar包了，因此采用docker方式进行部署

2. 添加依赖在需要监控的服务

   ```groovy
   compile('org.springframework.cloud:spring-cloud-starter-sleuth')
   compile('org.springframework.cloud:spring-cloud-starter-zipkin')
   ```

3. 添加配置，在`application.yml`添加zipkin服务端地址，和采样比例

   ```yaml
   spring:
     zipkin:
       base-url: http://10.14.0.7:14009/
     sleuth:
       web:
         client:
           enabled: true
       sampler:
         probability: 1.0 #采样比例0～1之间，1全部采样
   ```

4. 访问http://10.14.0.7:14009/进行测试

##### 测试结果

1. 在eureka服务注册端添加没监控到请求
2. 启动两个一样的服务提供者，端口不一致，以一个服务展示，但是能看到两个客户端
3. 请求之后才能监控到

## 方式二docker-zipkin+rabbitMQ+sleuth(暂时未成功)

```mermaid
graph LR
请求-->微服务客户端-->sleuth采集请求-->mq发送请求的信息-->docker-zipkin接受并展示
```

1. 修改docker-compose部署添加环境变量(目测该镜像还不支持改环境变量)

   ```yaml
   version: '3'

   services:
     zipkin:
       restart: always
       image: openzipkin/zipkin
       environment:
         RABBIT_ADDRESSES: mq的地址
         RABBIT_PASSWORD: mq的密码
         RABBIT_USER: mq的用户名
       ports:
         - "14009:9411"
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == worker]
   ```

2. 修改客户端依赖

   ```groovy
   compile('org.springframework.cloud:spring-cloud-starter-sleuth')
   //compile('org.springframework.cloud:spring-cloud-starter-zipkin')  //注释这句
   compile('org.springframework.boot:spring-boot-starter-amqp')
   ```

3. 修改配置文件

   ```yaml
   #  zipkin:
   #    base-url: http://10.14.0.7:14009/
     sleuth:
       web:
         client:
           enabled: true
       sampler:
         probability: 1.0 #采样比例0～1之间，1全部采样
     rabbitmq:
       port: 14002
       host: 10.14.0.1
       username: root
       password: adminroot
   ```

4. 测试失败，读不到服务，通过看docker-zipkin似乎是这里的mq没启动起

### 数据持久化zipkin+mysql

待更新。。。







参考:[Baeldung-SpingCould-Sleuth](http://www.baeldung.com/spring-cloud-sleuth-single-application)

[史上最简单的 SpringCloud 教程 | 终章](https://blog.csdn.net/forezp/article/details/70148833)

[Spring Cloud（十二）：分布式链路跟踪 Sleuth 与 Zipkin【Finchley 版】](https://windmt.com/2018/04/24/spring-cloud-12-sleuth-zipkin/)



