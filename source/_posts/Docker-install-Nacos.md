---
title: Docker-install-Nacos
date: 2021-04-23 11:40:43
updated: 2021-04-23 11:47:43
categories: Docker
tags: [Docker,Nacos]
---

# 简介

Nacos 致力于帮助您发现、配置和管理微服务。Nacos 提供了一组简单易用的特性集，帮助您快速实现动态服务发现、服务配置、服务元数据及流量管理。

主要作用替代spring cloud的注册中心和配置中心

[官方文档](https://nacos.io/zh-cn/docs/what-is-nacos.html)

依赖关系：nacos依赖与mysql的数据库(也可以是其他数据库)作为存储

访问：ip+端口，默认登陆用户名密码为nacos/nacos

[docker部署脚本](https://github.com/nacos-group/nacos-docker)：

```properties
version: '3'
services:
  mysql:
    image: nacos/nacos-mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: adminroot
      MYSQL_DATABASE: xk-config
      MYSQL_USER: nacos
      MYSQL_PASSWORD: nacos
    ports:
      - 14050:3306
#    volumes:
#      - "/home/dockerdata/v-dev/mysql:/var/lib/mysql"      
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
  nacos:
    image: nacos/nacos-server:2.0.0-bugfix
    restart: on-failure
    environment:
      PREFER_HOST_MODE: hostname
      MODE: standalone
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: mysql
      MYSQL_SERVICE_DB_NAME: xk-config
      MYSQL_SERVICE_PORT: 3306
      MYSQL_SERVICE_USER: nacos
      MYSQL_SERVICE_PASSWORD: nacos
#    volumes:
#      - /home/dockerdata/v-dev/nacos/standalone-logs/:/home/nacos/logs
#      - /home/dockerdata/v-dev/nacos/init.d/custom.properties:/home/nacos/init.d/custom.properties
    ports:
      - 14051:8848
```



