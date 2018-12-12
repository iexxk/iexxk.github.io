---
title: Dubbo-Gradle-Config
date: 2018-05-16 23:29:07
updated: 2018-12-12 10:47:58
categories: Dubbo
tags: [Dubbo,Gradle]
---

#### 配置方式一`xml`

在resources目录`dubbo-provider.xml`配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <!--该提供者服务名称-->
    <dubbo:application name="dubbo-provider"/>
    <!--组播模式的注册中心，推荐用zookeeper-->
    <!--<dubbo:registry address="zookeeper://10.14.1.7:2181"/>-->
    <!--暴露的端口服务-->
    <dubbo:protocol name="dubbo" port="20880"/>
    <!--声明暴露服务公共接口类-->
    <dubbo:service interface="exxk.dubbo.commonimpl.DemoService" ref="demoService"/>
    <!--提供者实现类-->
    <bean id="demoService" class="exxk.dubbo.provider.impl.DemoServiceImpl"/>
</beans>
```

需要在dubbo启动器指向xml名字

```java
ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(
                new String[]{"dubbo-provider.xml"}); //读取dubbo配置文件
        context.start();
```

#### 配置方式二`dubbo.properties`

注：配置文件名字是固定的

```properties
dubbo.registry.address=zookeeper://10.14.1.7:2181
```

#### 配置方式三`jvm`

注：gradle application task run启动vm设置无效

```
-Ddubbo.registry.address=zookeeper://10.14.1.7:2181
```

### 覆盖策略

JVM>XML>Properties其中jvm优先级最高