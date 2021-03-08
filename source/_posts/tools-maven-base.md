---
title: Tools-Maven-Base
date: 2018-06-25 10:53:19
updated: 2021-02-01 20:21:50
categories: Tools
tags: [Tools,maven]
---

### maven基础

``clean install -DskipTests=true` 清理打包

`clean install -DskipTests=true -pl app -am` 清理 打包安装 跳过测试 单模块（app）

`tomcat7:run` 用内置tomcat运行jar

```bash
#解决maven仓库明明有包，但是idea下载不下来，可以手动执行命令进行下载，执行前先清理本地仓库目录
mvn dependency:get -DremoteRepositories=https://repo1.maven.org/maven2 -DgroupId=org.java-websocket -DartifactId=Java-WebSocket -Dversion=1.3.8
```



##### 注意

`clean`再运行时清理会报错，所以需要先当掉

