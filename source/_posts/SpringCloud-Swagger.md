---
title: SpringCloud-Swagger
date: 2021-06-04 13:53:36
updated: 2021-06-04 15:55:13
categories: SpringCloud
tags: [SpringCloud,Swagger]
---

## Swagger 整合knife4j

[ruoyi-cloud/cloud/swagger](http://doc.ruoyi.vip/ruoyi-cloud/cloud/swagger.html#%E5%9F%BA%E6%9C%AC%E4%BB%8B%E7%BB%8D)

[knife4j](https://xiaoym.gitee.io/knife4j/action/aggregation-nacos.html)

### Spring Cloud Gateway集成Knife4j

在xkiot-common-swagger的pom.xml添加如下依赖

```xml
         <dependency>
            <groupId>com.github.xiaoymin</groupId>
            <artifactId>knife4j-micro-spring-boot-starter</artifactId>
            <version>2.0.8</version>
        </dependency>
```

然后在xkiot-gateway的pom.xml添加如下依赖

```xml
				<dependency>
            <groupId>com.github.xiaoymin</groupId>
            <artifactId>knife4j-spring-boot-starter</artifactId>
            <version>2.0.8</version>
        </dependency>
```

原生swagger访问`http://{网关ip}:{port}/swagger-ui.html`通过网关进行访问，里面可以进行选择切换服务

整合knife4j后访问`http://{网关ip}:{port}/doc.html`

