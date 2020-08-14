---
title: SpringCould-Bus
date: 2018-04-22 17:19:26
updated: 2020-08-11 16:03:17
categories: Spring
tags: [SpringCould,Bus]
---

 SpringCould Bus是将分布式的节点用轻量的消息代理连接起来。用于服务间广播、通信、监控等。

该篇实现：通过bus实现配置修改后通知服务更改

### 步骤

1. 在configclient的基础上添加依赖

   ```java
   compile('org.springframework.cloud:spring-cloud-starter-bus-amqp')
   ```

2. 在`Hicontroller`类添加注解`@RefreshScope`

3. 在配置文件添加mq的服务器地址，和开启刷新

   ```yaml
   spring:  
     rabbitmq:
       host: 112.74.51.136
       port: 14002
       username: root
       password: adminroot
   management:
     endpoints:
       web:
         exposure:
           include: ["health","info","bus-refresh"]
   ```

4. 测试，依次运行注册中心、配置中心、该服务，然后访问接口，然后修改git config下的配置信息，然后访问接口，还是没变，需要调用`127.0.0.1:8097/actuator/bus-refresh?destination=config-client:8097`其中的`config-client:8097`是指定更新那台服务，也可以不指定参数，默认就是更新所有，然后在访问测试接口，发现已经配置已经改变了。

### 架构优化

可以在config-server添加config-client的配置，这样就可以调配置刷新`127.0.0.1:8096/actuator/bus-refresh/`接口，刷新所有配置客户端的配置了，注意依赖要加上 `compile('org.springframework.cloud:spring-cloud-starter-config')`config-client的配置依赖，因为config-client的依赖和`config-server`的`bus-refresh`接口不一样

![image-20200811155609870](http://gt163.cn:14033/blog/20200811155613.png)

