---
title: SpringCould-hystrix
date: 2018-04-13 00:12:23
updated: 2018-04-13 00:12:23
categories: Spring
tags: [SpringCould,hystrix]
---

### 在ribbon+restTemplate方式使用熔断器hystrix

阻止服务故障的“雪崩”效应(我简称保险)

1. 在`ribbonrest`项目上添加`compile('org.springframework.cloud:spring-cloud-starter-netflix-hystrix')`该依赖(这里用的gradle,maven做相应格式修改)，或者直接新建一个项目勾选如下

   - [x] web->web
   - [x] Could discovery-> eureka server
   - [x] Could routing->ribbon
   - [x] Could Circuit Breaker->Hystrix

2. 在`application`启动类添加一个注解`@EnableHystrix`拉上保险开关

3. 修改服务调用类`HelloService`

   ```java
   @Service
   public class HelloService {
       @Autowired
       RestTemplate restTemplate;

       @HystrixCommand(fallbackMethod = "hiError") //调用发生错误就调用hiError方法
       public String hiService(String name){
           //eureka-client为服务提供者的spring.application.name=eureka-client
          return restTemplate.getForObject("http://eureka-client/hi?name="+name,String.class);
       }
       //发生错误调用的方法
       public String hiError(String name) {
           return "hi,"+name+",sorry,error!";
       }
   }
   ```

4. 启动该服务(8093),然后访问http://127.0.0.1:8093/resthi?name=32，然后再停止两台服务提供者的其中一台，然后刷新一台提示错误，一台正常访问

   | 启动顺序                                                 | 访问结果                               | 再启动  | 结果             |
   | -------------------------------------------------------- | -------------------------------------- | ------- | ---------------- |
   | 注册中心-服务提供者(1和2)-服务消费者                     | 2台交替访问                            |         |                  |
   | 注册中心-服务提供者(1)-服务消费者-服务提供者(2)          | 1能访问                                |         |                  |
   | 注册中心-服务提供者(1和2)-服务消费者-停止1               | 1抛异常,2正常访问                      | 再启动1 | 恢复时间慢       |
   | 注册中心-服务提供者(1和2)-服务消费者(开启了熔断器)-停止1 | 1返回熔断器自定义的错误信息，2正常访问 | 再启动1 | 马上可以交替访问 |

### 在feign模式使用熔断器

Feign是自带断路器的

1. 新建`SchedualServiceHiHystric`实现服务调用的接口

   ```Java
   @Component
   public class SchedualServiceHiHystric implements FeignSchedualService{
       @Override
       public String sayHiFromEurekaClient(String name) {
           return "sorry "+name;
       }
   }
   ```

2. 在服务调用接口的`@FeignClient`添加`fallback`指向刚刚实现这个接口的类

   ```java
   @FeignClient(value = "eureka-client",fallback = SchedualServiceHiHystric.class) //指定调用那个服务（服务名spring.application.name）
   public interface FeignSchedualService {
       @RequestMapping(value = "/hi",method = RequestMethod.GET)  //指定调用eureka-client服务的那个接口
       String sayHiFromEurekaClient(@RequestParam(value = "name") String name);
   }
   ```

   ​