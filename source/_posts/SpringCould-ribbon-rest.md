---
title: SpringCould 服务提供者与消费者
date: 2018-04-11 21:00:20
updated: 2018-04-12 01:52:02
categories: Spring
tags: [Springboot,SpringCould,ribbon,rest]
---

### 服务调用方式

- [x] 第一种方式：ribbon+restTemplate
- [ ] 第二种方式：feign(默认集成ribbon)

ribbon是一个负载均衡客户端，可以很好的控制htt和tcp的一些行为。

### 建立服务提供者

1. 在`eurekaclient`添加一个`HelloControl`接口类

   ```java
   @RestController
   public class HelloControl {
       
       @Value("${server.port}")
       String port;
       
       @RequestMapping("/hi")
       public String home(@RequestParam String name) {
           return "hi "+name+",i am from port:" +port;
       }
   }
   ```

2. 启动两个`eurekaclient`配置vm启动参数`-Dserver.port=8098`端口分布为8099和8098。

### 建立服务消费者

1. 新建springboot项目勾选如下

   - [x] web->web
   - [x] Could discovery-> eureka server
   - [x] Could routing->ribbon

2. 在`RibbonrestApplication`启动类添加注解`@EnableEurekaClient`

3. 在`Application.yml`配置文件添加内容：

   ```yaml
   server:
     port: 8093
   spring:
     application:
       name: ribbon-client
   eureka:
     client:
       service-url:
         defaultZone: http://127.0.0.1:8091/eureka/ #注意要加eureka，不然找不到
   ```

4. 在`RibbonrestApplication`启动类添加负载均衡

   ```java
   @Bean  //spring ioc bean 依赖注入知识点(待补充)
   @LoadBalanced //负载均衡
   RestTemplate restTemplate(){
       return new RestTemplate();
   }
   ```

5. 新建`HelloService`类消费服务

   ```Java
   @Service
   public class HelloService {
       @Autowired
       RestTemplate restTemplate;

       public String hiService(String name){
    //eureka-client为服务提供者的spring.application.name=eureka-client
          return restTemplate.getForObject("http://eureka-client/hi?name="+name,String.class); //该url为服务提供者提供的接口
       }
   }
   ```

6. 调用`HelloService`的服务，新建一个`HelloControler`类

   ```Java
   @RestController
   public class HelloControler {
       @Autowired
       HelloService helloService;
       @RequestMapping(value = "/resthi") //访问入口
       public String hi(@RequestParam String name){
           return helloService.hiService(name); //调用消费服务
       }
   }
   ```

7. 访问[http://127.0.0.1:8093/resthi?name=32](http://127.0.0.1:8093/resthi?name=32)这个服务消费者提供的接口，不停刷新可以看到端口的变化，就说明了负载均衡起作用了。

### 总结图示

```sequence
Note left of eurekaClient8099/8098: 服务提供者(n个)
Note left of eurekaService8091: 服务注册中心
Note left of ribbonClient8093: 服务消费者
eurekaClient8099/8098-->eurekaService8091: 注册
ribbonClient8093-->eurekaService8091: 注册
ribbonClient8093-->eurekaClient8099/8098: 通过ribbon负载均衡调用服务8099/8098
```



