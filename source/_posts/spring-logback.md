---
title: spring logback
date: 2020-09-03 15:50:23
updated: 2021-04-13 10:27:30
categories: Spring
tags: [Spring,Logback]
---

# spring logback 简介

### 依赖图

可以发现logback在`spring-boot-starter`依赖里面，所以引入了springboot都自带logback

```mermaid
graph LR
logback-->spring-boot-starter-logging-->spring-boot-starter
```

```yaml
+--- org.springframework.boot:spring-boot-starter -> 2.2.2.RELEASE
|    +--- org.springframework.boot:spring-boot:2.2.2.RELEASE
|    |    +--- org.springframework:spring-core:5.2.2.RELEASE
|    |    |    \--- org.springframework:spring-jcl:5.2.2.RELEASE
|    |    \--- org.springframework:spring-context:5.2.2.RELEASE
|    |         +--- org.springframework:spring-aop:5.2.2.RELEASE
|    |         |    +--- org.springframework:spring-beans:5.2.2.RELEASE
|    |         |    |    \--- org.springframework:spring-core:5.2.2.RELEASE (*)
|    |         |    \--- org.springframework:spring-core:5.2.2.RELEASE (*)
|    |         +--- org.springframework:spring-beans:5.2.2.RELEASE (*)
|    |         +--- org.springframework:spring-core:5.2.2.RELEASE (*)
|    |         \--- org.springframework:spring-expression:5.2.2.RELEASE
|    |              \--- org.springframework:spring-core:5.2.2.RELEASE (*)
|    +--- org.springframework.boot:spring-boot-autoconfigure:2.2.2.RELEASE
|    |    \--- org.springframework.boot:spring-boot:2.2.2.RELEASE (*)
|    +--- org.springframework.boot:spring-boot-starter-logging:2.2.2.RELEASE
|    |    +--- ch.qos.logback:logback-classic:1.2.3 #可以看到在springboot里面自带
|    |    |    +--- ch.qos.logback:logback-core:1.2.3
|    |    |    \--- org.slf4j:slf4j-api:1.7.25 -> 1.7.29
|    |    +--- org.apache.logging.log4j:log4j-to-slf4j:2.12.1
|    |    |    +--- org.slf4j:slf4j-api:1.7.25 -> 1.7.29
|    |    |    \--- org.apache.logging.log4j:log4j-api:2.12.1
|    |    \--- org.slf4j:jul-to-slf4j:1.7.29
|    |         \--- org.slf4j:slf4j-api:1.7.29
|    +--- jakarta.annotation:jakarta.annotation-api:1.3.5
|    +--- org.springframework:spring-core:5.2.2.RELEASE (*)
|    \--- org.yaml:snakeyaml:1.25
```

## `logback-spring.xml`介绍

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Logback configuration. See http://logback.qos.ch/manual/index.html -->
<!--
scan：当此属性设置为true时，配置文件如果发生改变，将会被重新加载，默认值为true。
scanPeriod：设置监测配置文件是否有修改的时间间隔，如果没有给出时间单位，默认单位是毫秒当scan为true时，此属性生效。默认的时间间隔为1分钟。
debug：当此属性设置为true时，将打印出logback内部日志信息，实时查看logback运行状态。默认值为false。
-->
<configuration scan="true" scanPeriod="10 seconds" debug="false">
    <!--服务名称，通过读取spring配置项spring.application.name-->
    <springProperty scope="context" name="APP_NAME" source="spring.application.name" />
    <!--日志输出类型,可在配置文件通过spring.cloud.config.logback-profile进行设置日志输出类型   -->
    <springProperty scope="context" name="LOG_TYPE" source="spring.cloud.config.logback-profile" />
    <!--定义日志的目录，logs为项目根目录下logs目录 -->
    <property name="LOG_PATH" value="logs" />
    <!--定义日志的文件名 -->
    <property value="${LOG_PATH}/${APP_NAME}.log" name="LOG_FILE_NAME" />
    <!-- %d{yyyy-MM-dd}：按天进行日志滚动 %i：当文件大小超过maxFileSize时，按照i进行文件滚动   -->
    <property value="${LOG_PATH}/${APP_NAME}-%d{yyyy-MM-dd}-%i.log" name="LOG_FILE_NAME_PATTERN" />
    <!--定义日志的格式化标准 -->
    <property name="LOG_FORMAT" value="%d{yyyy-MM-dd HH:mm:ss.SSS} [ %thread ] - [ %-5level ] [ %logger{50} : %line ] - %msg%n" />

    <!-- 文件输出： 滚动记录文件，先将日志记录到指定文件，当符合某个条件时，将日志记录到其他文件 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 指定日志文件的名称 -->
        <file>${LOG_FILE_NAME}</file>
        <!--日志文件分割机制-->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_FILE_NAME_PATTERN}</fileNamePattern>
            <!--日志保留天数-->
            <MaxHistory>30</MaxHistory>
            <!--当天日志当大于100M进行分割-->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <!-- 日志输出格式： -->
        <layout class="ch.qos.logback.classic.PatternLayout">
            <pattern>${LOG_FORMAT}</pattern>
        </layout>
    </appender>

    <!--控制台输出:也就是前端显示输出 -->
    <appender name="stdout" class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <pattern>${LOG_FORMAT}</pattern>
        </layout>
    </appender>

    <!-- 定义不同的包，不同的日志级别(TRACE < DEBUG < INFO < WARN < ERROR),additivity生效级别true都有效(所有日志输出类型，包含默认的)，false只是当前（当前配置的输出日志类型）有效 -->
    <logger name="com.exxk" level="debug" />
    <logger name="org.springframework" level="debug" additivity="false"></logger>

    <!--选择那个日志输出类型，对应上面的appender，支持多个同时选择 -->
    <root level="info">
        <!--stdout设置为默认输出类型，不需要的输出类型可以直接注释-->
        <appender-ref ref="stdout" />
        <!--通过application配置文件的spring.cloud.config.logback-profile配置项进行指定加载那个日志输出类型，值为appender的name  -->
        <appender-ref ref="${LOG_TYPE}" />
    </root>
</configuration>
```

`application.properties`

```properties
spring.application.name=testDemo
#指定那个输出类型
spring.cloud.config.logback-profile=FILE
```

# log 日志脱敏和超长日志处理

#### 需求：

因为日志里面含有大量的base64的图片数据，各处都有打印，导致日志过大，日志不美观排查问题不方便





### 参考

[logback-spring.xml](https://www.jianshu.com/p/6f093b0b0c8a)

[一般人不敢动系列之—基于logback的日志“规范”和“脱敏”](https://cloud.tencent.com/developer/article/1650600)

