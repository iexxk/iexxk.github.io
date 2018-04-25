---
title: SpringCould-feign服务消费
date: 2018-04-12 22:46:03
updated: 2018-04-25 20:47:32
categories: Spring
tags: [Springboot,SpringCould,feign]
---

### 服务调用方式

- [ ] 第一种方式：ribbon+restTemplate
- [x] 第二种方式：feign(默认集成ribbon)

Feign 采用的是基于接口的注解，默认整合了ribbon(负载均衡)。

### [建立服务提供者](http://bolg.iexxk.com/2018/04/11/SpringCould-ribbon-rest/)

### 建立服务消费者

1. 新建springboot项目勾选如下

   - [x] web->web
   - [x] Could discovery-> eureka server
   - [x] Could routing->feign

2. 在`application.yml`添加如下配置

   ```yaml
   server:
     port: 8094
   spring:
     application:
       name: feign-client
   eureka:
     client:
       service-url:
         defaultZone: http://127.0.0.1:8091/eureka/ #注意要加eureka，不然找不到
   ```

3. 在`EurekafeignApplication.java`类添加注解`@EnableFeignClients`标记为Feign服务

4. 新建一个服务调用接口类`FeignSchedualService.java`

   ```java
   @FeignClient(value = "eureka-client") //指定调用那个服务（服务名spring.application.name）
   public interface FeignSchedualService {
       @RequestMapping(value = "/hi",method = RequestMethod.GET)  //指定调用eureka-client服务的那个接口
       String sayHiFromEurekaClient(@RequestParam(value = "name") String name);
   }
   ```

5. 新建一个对外访问`HiController.java`类

   ```Java
   @RestController
   public class HiController {
       @Autowired
       FeignSchedualService feignSchedualService;
       
       @RequestMapping(value = "/sayhi",method = RequestMethod.GET)
       public String sayHi(@RequestParam String name){
           return feignSchedualService.sayHiFromEurekaClient(name);
       }
   }
   ```

6. 依次启动eureka注册中心、eureka服务提供者(2个以上)、feign服务消费者

7. 访问[http://127.0.0.1:8094/sayhi?name=32](http://127.0.0.1:8094/sayhi?name=32)就可以看到返回不同的端口了

