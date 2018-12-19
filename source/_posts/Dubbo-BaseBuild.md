---
title: Dubbo-BaseBuild
date: 2018-05-08 15:46:14
updated: 2018-12-12 10:47:58
categories: Dubbo
tags: [Dubbo]
---



[dubbo官网](https://dubbo.incubator.apache.org/)/[dubbo仓库地址](https://mvnrepository.com/artifact/com.alibaba/dubbo)

1. 环境准备新建一个空的project，分别三个model

   | model名称        | model类型        | 说明                                                     |
   | ---------------- | ---------------- | -------------------------------------------------------- |
   | common_interface | java类型空项目   | 用于存放服务提供者和服务消费者的公共接口，避免写两次而已 |
   | consumer         | springboot空项目 | 消费者服务依赖`common_interface `  model                 |
   | provider         | springboot空项目 | 提供者服务依赖`common_interface `  model                 |

2. 上面项目建立好，model依赖关系加好之后，下面开始引入dubbo框架

3. 两个springboot项目都引入dubbo依赖这里用的gradle，仓库地址可以去[dubbo仓库地址](https://mvnrepository.com/artifact/com.alibaba/dubbo)查看

   ```groovy
   compile group: 'com.alibaba', name: 'dubbo', version: '2.6.1'
   ```

4. 在`common_interface`项目中添加一个接口类

   ```java
   package exxk.dubbo.commonimpl;
   
   public interface DemoService {
       String sayHello(String name);
   }
   ```

5. 在`provider`项目中实现`DemoService`接口，在java目录下新建impl包，并添加一个`DemoServiceImpl`实现类

   ```java
   package exxk.dubbo.provider.impl;
   
   import exxk.dubbo.commonimpl.DemoService;
   
   public class DemoServiceImpl implements DemoService{
       @Override
       public String sayHello(String name) {
           return "hello"+ name;
       }
   }
   ```

6. 在`provider`项目中`resource`目录下添加一个dubbo配置文件`dubbo-provider.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <beans xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
          xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">
       <!--该提供者服务名称-->
       <dubbo:application name="dubbo-provider"/>
       <!--组播模式的注册中心，推荐用zookeeper-->
       <dubbo:registry address="multicast://224.5.6.7:1234"/>
       <!--暴露的端口服务-->
       <dubbo:protocol name="dubbo" port="20880"/>
       <!--声明暴露服务公共接口类-->
       <dubbo:service interface="exxk.dubbo.commonimpl.DemoService" ref="demoService"/>
       <!--提供者实现类-->
       <bean id="demoService" class="exxk.dubbo.provider.impl.DemoServiceImpl"/>
   </beans>
   ```

7. 在`provider`项目中`java`目录下添加一个dubbo 启动类`Provider.java`

   ```java
   package exxk.dubbo.provider;
   
   import org.springframework.context.support.ClassPathXmlApplicationContext;
   
   public class Provider {
       public static void main(String[] args) throws Exception {
           ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(
                   new String[]{"dubbo-provider.xml"}); //读取dubbo配置文件
           context.start();
           //按任何键推出
           System.in.read();
       }
   }
   ```

8. 上面的服务提供者基本完成，然后启动服务提供者，直接运行`Provider.java`静态方法即可

9. 在`consumer`项目中`resource`目录下添加一个dubbo配置文件`dubbo-consumer.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <beans xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
          xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">
       <dubbo:application name="dubbo-consumer"/>
       <!--注册中心地址（多播）-->
       <dubbo:registry address="multicast://224.5.6.7:1234"/>
       <dubbo:reference id="demoService" interface="exxk.dubbo.commonimpl.DemoService"/>
   </beans>
   ```

10. 在`consumer`项目中`java`目录下添加一个dubbo 启动类`Consumer.java`

  ```java
  package exxk.dubbo.consumer;
  
  import exxk.dubbo.commonimpl.DemoService;
  import org.springframework.context.support.ClassPathXmlApplicationContext;
  
  public class Consumer {
      public static void main(String[] args) throws Exception{
          ClassPathXmlApplicationContext context=new ClassPathXmlApplicationContext(
                  new String[]{"dubbo-consumer.xml"});
          context.start();
          DemoService demoService= (DemoService) context.getBean("demoService");
          String hello= demoService.sayHello("world");
          System.out.print(hello);
      }
  }
  ```

11. 启动`consumer`服务消费者项目，这里用debug模式运行`Consumer.java`在里面打断点，主要是日志不好找，因此debug

### 基于springboot优化启动类

在springboot启动类添加dubbo启动，去掉默认的dubbo启动

1. 最直接的是把dubbo启动类的配置xml内容直接放到application启动类

   ```java
   @SpringBootApplication
   public class ProviderApplication {
   	public static void main(String[] args) {
   		SpringApplication.run(ProviderApplication.class, args);
   		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(
                   new String[]{"dubbo-provider.xml"}); //读取dubbo配置文件
           context.start();
           //同步锁，保持该线程一直运行
           synchronized (Provider.class){
               while(true){
                   try {
                       Provider.class.wait();
                   }catch (Exception e){
                       System.out.print("synchronized===:"+e);
                   }
               }
           }
   	}
   }
   ```

2. 这种当然不优雅，可以直接把xml配置文件配置到注解`@ImportResource`上

   ```java
   @SpringBootApplication
   public class ProviderApplication {
   	public static void main(String[] args) {
   		SpringApplication.run(ProviderApplication.class, args);
           //同步锁，保持该线程一直运行
           synchronized (Provider.class){
               while(true){
                   try {
                       Provider.class.wait();
                   }catch (Exception e){
                       System.out.print("synchronized===:"+e);
                   }
               }
           }
   	}
   }
   ```

3. 代码是少了，但是据说，dubbo包含web框架，会让springboot当成web程序运行，这里自定义`SpringApplicationBuilder`禁用web

   ```java
   @SpringBootApplication
   public class ProviderApplication {
   	public static void main(String[] args) {
   		ApplicationContext context= new SpringApplicationBuilder()
   				.sources(ProviderApplication.class)
   				.web(WebApplicationType.NONE)  //禁用web服务
   				.run(args);
           //同步锁，保持该线程一直运行
           synchronized (Provider.class){
               while(true){
                   try {
                       Provider.class.wait();
                   }catch (Exception e){
                       System.out.print("synchronized===:"+e);
                   }
               }
           }
   	}
   }
   ```

4. 同步锁线程也换种方式实现,利用同步工具类`CountDownLatch`,该工具类的大概作用就是有等待指定线程（数）执行完了，再执行

   ```java
   @SpringBootApplication
   @ImportResource({"classpath:dubbo-provider.xml"})
   public class ProviderApplication {
   
   	@Bean
   	public CountDownLatch closeLatch() {
   		return new CountDownLatch(1);
   	}
   
   	public static void main(String[] args) throws InterruptedException {
   		//SpringApplication.run(ProviderApplication.class, args);
   		ApplicationContext context= new SpringApplicationBuilder()
   				.sources(ProviderApplication.class)
   				.web(WebApplicationType.NONE)  //禁用web服务
   				.run(args);
   
   		CountDownLatch closeLatch=context.getBean(CountDownLatch.class);
   		closeLatch.await(); //等待所有子线程完成
   	}
   }
   ```

5. 最后删除旧的启动器，到此大功告成