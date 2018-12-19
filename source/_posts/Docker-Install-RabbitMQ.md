---
title: Docker-Install-RabbitMQ
date: 2018-04-10 12:10:51
updated: 2018-12-12 10:47:58
categories: Docker
tags: [Docker swarm,RabbitMQ]
---

### RabbitMQ安装

[docker-hub/rabbitmq](https://hub.docker.com/r/_/rabbitmq/)

```yaml
version: '3'
services:
  rabbitmq:
    image: rabbitmq
    restart: always
    hostname: xuanps #节点名字
    environment:
      RABBITMQ_DEFAULT_USER: root #设置用户名
      RABBITMQ_DEFAULT_PASS: ******* #设置密码
    ports:
      - 14002:5672
    volumes:
      - "/dockerdata/v-rabbitmq:/var/lib/rabbitmq"
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == xuanps]
```

### springboot 连接mq

```Xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

mq连接配置`application.yml`

```yaml
spring:
  rabbitmq:
    host: 112.74.51.136
    port: 14002
    username: root
    password: ********
```

mq发送数据（测试类）

```Java
@Autowired
private AmqpTemplate rabbitTemplate;
@Test
public void send() {
    String context="hello"+new Date();
    System.out.print("send context:"+context);
    rabbitTemplate.convertAndSend("hello",context);
}
```

mq配置类`MqConfig.java`

```Java
import org.springframework.amqp.core.Queue; //注意不要导错包
@Configuration
public class MqConfig {
    @Bean
    public Queue helloQueue(){
        return new Queue("hello");
    }
}
```

mq接受数据类`MqReceiver.java`

```java
@Component  //注解必须加
@RabbitListener(queues = "hello")
public class MqReceiver {
    @RabbitHandler
    public void process(String hello){
        System.out.print("receiver:"+hello);
    }
}
```

测试效果：先启动主程序，再点击测试类发送，主程序就可以接收到消息了。（先发送后启动主程序是接受不到的）

