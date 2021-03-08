---
title: SpringBoot-Note
date: 2018-05-07 16:14:45
updated: 2018-12-12 10:47:58
categories: Spring
tags: [SpringBoot,笔记,基础]
---

## [Spring Boot干货系列总纲](http://tengj.top/2017/04/24/springboot0/) 阅读笔记

### 配置文件解析

默认`src/main/resources`目录下，两种格式`application.properties`或`application.yml`

自定义属性,在配置文件`application.properties`定义`diy.name="hello" `,在使用的地方加上注解

```java
 @Value("${diy.name}")
 private  String name;
```

自定义配置类,需要在springboot入口类添加`@EnableConfigurationProperties({ConfigBean.class})`

```java
@ConfigurationProperties(prefix = "diy")
public class ConfigBean {
    private String name;
    private String want;
    // 省略getter和setter
}
```





