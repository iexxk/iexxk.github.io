---
title: Docker-Install-RabbitMQ
date: 2018-04-10 12:10:51
updated: 2019-12-05 11:10:45
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

### centos7 install RabbitMQ

1. 首先下载[安装包](http://47.98.114.63:14018/s/J9B2LHJqZkPCGmG):erlang、socat、rabbitmq以此用`rpm -ivh <>`安装这三个

2. 新建修改配置文件`vi /etc/rabbitmq/rabbitmq.config`

   ```properties
   [
   {rabbit, [{tcp_listeners, [5672]}, {loopback_users, ["admin"]}]}
   ].
   ```

3. 启动rabbitmq服务

   ```bash
   #启动服务
   systemctl start rabbitmq-server
   #查看状态
   systemctl status rabbitmq-server
   ```

4. 配置远程管理web界面

   ```bash
   rabbitmq-plugins enable rabbitmq_management
   rabbitmq-plugins enable rabbitmq_stomp
   rabbitmq-plugins enable rabbitmq_web_stomp
   ```

5. 配置用户远程访问

   ```bash
   #新建用户test密码test
   rabbitmqctl add_user test test
   rabbitmqctl set_user_tags test administrator
   rabbitmqctl set_permissions -p / test '.*' '.*' '.*'
   ```

6. 重启rabbitmq服务执行`systemctl restart rabbitmq-server`

7. 添加防火墙访问端口

   ```bash
   #添加15672端口
   firewall-cmd --zone=public --add-port=15672/tcp --permanent
   #加载配置
   firewall-cmd --reload
   #查看配置是否生效
   firewall-cmd --list-all
   ```

8. 测试，浏览器访问`http://<服务器ip>:15672/`使用test,test用户密码登陆



### 常见问题

问题1：`.erlang.cookie must be accessible by owner only `不断重启

解决：删除整个挂载目录，包括`rabbitmq`，然后重建



