---
title: Tools-Maven-Base
date: 2018-06-25 10:53:19
updated: 2018-06-25 10:53:19
categories: Tools
tags: [Tools,maven]
---

### maven基础

``clean install -DskipTests=true` 清理打包

`clean install -DskipTests=true -pl app -am` 清理 打包安装 跳过测试 单模块（app）

`tomcat7:run` 用内置tomcat运行jar

##### 注意

`clean`再运行时清理会报错，所以需要先当掉