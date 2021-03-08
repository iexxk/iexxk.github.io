---
title: Dubbo-Gradle-Build
date: 2018-05-14 14:56:08
updated: 2018-12-12 10:47:58
categories: Dubbo
tags: [Dubbo,Gradle]
---

源码：https://github.com/xuanfong1/DubboLearning

1. 新建目录` mkdir DubboLearning`,然后`cd Dubbolearning`进去之后执行`gradle init`初始化gradle项目

2. 新建三个子项目目录`mkdir library,provider,consumer `分别为公共依赖项目、提供者、消费者

3. 复制build.gradle到三个子项目目录

4. 分别为三个子项目创建目录`mkdir -p src/main/java,src/test/java,src/main/resources`

5. 修改顶级项目目录的setting.gradle添加三个子项目

   ```groovy
   include 'library'
   inclede 'provider'
   inclede 'consumer'
   ```

6. 复制项目helloworld的源码到项目目录

7. 然后修改顶级项目目录build.gradle

   ```groovy
   plugins {
       id "org.springframework.boot" version "2.0.1.RELEASE"
   }
   allprojects {
       repositories {
           jcenter() //将jcenter仓库配置到所有项目
       }
   }
   subprojects {
       version = '1.0' //设置版本号
   }
   configure(subprojects.findAll {it.name == 'provider' || it.name == 'consumer'} ) {

       apply plugin: 'java'
       apply plugin: 'eclipse'
       apply plugin: "org.springframework.boot"
       apply plugin: 'io.spring.dependency-management'

       group = 'exxk.dubbo'
       version = '0.0.1-SNAPSHOT'
       sourceCompatibility = 1.8

       dependencies {
           compile('org.springframework.boot:spring-boot-starter')
           compile group: 'com.alibaba', name: 'dubbo', version: '2.6.1'
           testCompile('org.springframework.boot:spring-boot-starter-test')
           compile project(':library')
       }
   }
   ```

   ​

### 额外

https://plugins.gradle.org/plugin/org.springframework.boot

```groovy
//低版本，动态
buildscript {
    ext {
        springBootVersion = '2.0.1.RELEASE'
    }
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
    }
}
//等效于
//高版本
plugins {
  id "org.springframework.boot" version "2.0.2.RELEASE"
}

```



报错：

```
Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/curator/RetryPolicy
	at com.alibaba.dubbo.remoting.zookeeper.curator.CuratorZookeeperTransporter.connect(CuratorZookeeperTransporter.java:26)
```

解决：添加依赖`compile group: 'org.apache.curator', name: 'curator-framework', version: '4.0.1'`