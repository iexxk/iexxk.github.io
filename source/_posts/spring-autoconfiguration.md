---
title: Spring AutoConfiguration
date: 2020-08-18 14:31:27
updated: 2020-08-18 16:33:26
categories: Spring
tags: [AutoConfiguration,Spring]
---

springboot的配置使用很简单，也经常用，下面就是常用的AutoConfiguration入口

```java
@EnableAutoConfiguration //启用自动配置
@ComponentScan
public class Application{}
```

但是这里主要讲下自动配置的禁用

## 如何禁用某些自动配置

### 需求场景

1. 在公共依赖里面引入了数据库的依赖，你会发现，某些项目不需要数据库，但是由于公共依赖，也得配置数据库的连接地址
2. 例如使用spring cloud config-bus热更新配置时，这个功能属于可选功能，因为有些环境可能不支持mq，但是不能每次打包都把依赖移除

###禁用设置

#### 启动文件的修改

主要是在启动类上面的`@EnableAutoConfiguration`注解添加参数`exclude`后面填入需要禁用的启动类，这种适合场景1，因为已经确定这个服务是不需要这个配置的了

```java
@EnableAutoConfiguration(exclude = {MongoAutoConfiguration.class, MongoDataAutoConfiguration.class})
@EnableConfigurationProperties
public class App {}
```

#### 配置文件的修改

在`application.properties`里面添加`spring.autoconfigure.exclude`这个配置项，这个就很灵活了，只需要修改配置文件，就可以开启或禁用某些功能

```properties
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration,org.springframework.boot.actuate.autoconfigure.metrics.amqp.RabbitMetricsAutoConfiguration,org.springframework.boot.actuate.autoconfigure.amqp.RabbitHealthIndicatorAutoConfiguration,org.springframework.boot.actuate.autoconfigure.health.HealthEndpointAutoConfiguration,org.springframework.cloud.bus.BusAutoConfiguration
```

### 常用的实战场景

禁用操作很简单，但是要找到合适的配置禁用，这就需要了解功能用到了那些自动配置项，下面介绍几个常用场景，需要禁用的自动配置类

```properties
#mongodb数据库 依赖 org.springframework.data:spring-data-mongodb
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration
#redis数据库 依赖 org.springframework.boot:spring-boot-starter-data-redis
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration
#rabbitMQ 依赖 org.springframework.boot:spring-boot-starter-amqp
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration
#springCloud-Bus 依赖org.springframework.cloud:spring-cloud-starter-bus-amqp
spring.autoconfigure.exclude=org.springframework.cloud.bus.BusAutoConfiguration,org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration
```





