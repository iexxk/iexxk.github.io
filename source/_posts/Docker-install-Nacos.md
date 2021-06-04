---
title: Docker-install-Nacos
date: 2021-04-23 11:40:43
updated: 2021-06-02 10:55:46
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



## docker swarm nacos指定容器虚拟IP自定义网络

在用nacos做为注册中心和配置中心时，如果部署模式是docker swarm模式时，由于容器内部多个网卡，默认随机eth0，就会导致这个ip是内部ip导致无法访问其他容器的服务

##### 解决

先看stack的网络，从下图可以看到用的网络是10.0.3开头的

[![2MY6df.png](https://z3.ax1x.com/2021/06/02/2MY6df.png)](https://imgtu.com/i/2MY6df)

因此可以进行设置优先网络

```yml
    environment:
      - spring.cloud.inetutils.preferred-networks=10.0.3
```

或者进入容器进行忽略网卡的设置，可以看到需要忽略到eth0，和eth2，只剩下需要的

[![2Mtyc9.png](https://z3.ax1x.com/2021/06/02/2Mtyc9.png)](https://imgtu.com/i/2Mtyc9)

因此配置参数如下：

```yml
 - spring.cloud.inetutils.ignored-interfaces=eth0.*,eth2.*
```

更多详细的配置见[Appendix A: Common application properties](https://cloud.spring.io/spring-cloud-commons/reference/html/appendix.html#common-application-properties)

测试网络的互访可以通过springcloud的心跳

```bash
wget http://10.0.3.194:9200/actuator/health -q -O -
```



