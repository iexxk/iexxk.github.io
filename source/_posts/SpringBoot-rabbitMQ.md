---
title: SpringBoot 动态添加监听 rabbitMQ 队列
date: 2020-07-10 16:32:40
updated: 2020-07-10 16:43:06
categories: SpringBoot
tags: [rabbitMQ]
---

### 需求

这里需要监听多个队列，而且运行途中可能会增加监听，或减少监听，因此实现需要采用`SimpleMessageListenerContainer`类

### 步骤

1. 添加gradle依赖

   ```groovy
    implementation 'org.springframework.boot:spring-boot-starter-amqp'
    compile 'cn.hutool:hutool-all:5.3.8'
   ```

2. 添加`application.properties`

   ```properties
   spring.rabbitmq.host=10.10.10.11
   spring.rabbitmq.port=14012
   spring.rabbitmq.username=test
   spring.rabbitmq.password=test
   spring.rabbitmq.virtual-host=/
   spring.rabbitmq.connection-timeout=5000
   spring.rabbitmq.countDownLatch=5
   spring.rabbitmq.webport=14013
   spring.rabbitmq.websocket-port=14014
   ```

3. 创建一个监听类`RbMQReceiverHandler.java`

   ```java
   /**
    * 监听接收消息
    */
   @Component
   public class RbMQReceiverHandler implements MessageListener {
       private final Logger log = LoggerFactory.getLogger(getClass());
   
       @Override
       public void onMessage(Message message) {
           log.info("====接收到" + message.getMessageProperties().getConsumerQueue() + "队列的消息=====");
           log.info(message.getMessageProperties().toString());
           log.info(new String(message.getBody()));
       }
   }
   ```

4. 创建一个`RabbitMQConfig.java`配置文件

   ```java
   @Configuration
   @Import(cn.hutool.extra.spring.SpringUtil.class)  //huTool添加，才能用getBean
   public class RabbitMQConfig {
   
       @Autowired
       RbMQReceiverHandler rbMQReceiverHandler;
   
       @Bean
       public SimpleMessageListenerContainer messageListenerContainer(ConnectionFactory connectionFactory) {
           SimpleMessageListenerContainer container = new SimpleMessageListenerContainer();
           container.setConnectionFactory(connectionFactory);
           container.setQueueNames("test1_staff");
           container.setMessageListener(rbMQReceiverHandler);
           return container;
       }
   }
   ```

5. 添加一个动态添加队列的接口

   ```java
   @RestController
   @RequestMapping("/queue")
   public class RbController {
   
       @PostMapping
       public String addQueue(@RequestParam String queueNmae) {
           SimpleMessageListenerContainer container = SpringUtil.getBean(SimpleMessageListenerContainer.class);//获取实例
           container.addQueueNames(queueNmae);
           return "add " + queueNmae + " ok";
       }
   
       @DeleteMapping
       public String delQueue(@RequestParam String queueNmae) {
           SimpleMessageListenerContainer container = SpringUtil.getBean(SimpleMessageListenerContainer.class);
           container.removeQueueNames(queueNmae);
           return "delete " + queueNmae + " ok";
       }
   }
   ```

6. 测试调用post 127.0.0.1:8080/queue 接口就能添加队列了，发送mq的消息没写测试方法，但是可以直接到mq的管理页面push一条消息进行测试

