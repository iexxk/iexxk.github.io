---
title: docker-ELK
date: 2020-08-20 16:17:51
updated: 2020-09-03 14:29:14
categories: Docker
tags: [ELK]
---

## [ELK/EFK简介](https://www.elastic.co/cn/)

E(Elasticsearch)+L(Logstash)+K(Kibana)

E(Elasticsearch)+F(Filebeat)+K(Kibana)

Redis/Mq/kafka大数据高提高弹性时候可选

```mermaid
graph LR
B(beats数据采集)-.->G([redis/mq/kafka])-.->L[Logstash数据管道/处理]-->E[Elasticsearch数据存储/索引]-->K[Kibana数据分析/显示]
B-->L
```

## Logstash

输入支持：tcp,http,file,beats,kafka,rabbitmq,redis,log4j,elasticsearch,jdbc,websocket

过滤器支持：grok,ruby,mutate,json

输出支持：elasticsearch,File,Emial,http,Kafka,Redis,MongoDB,Rabbitmq,Syslog,Tcp,Websocket,Zabbix,Stdout,Csv

## Filebeat

Filebeat主要用于数据采集，轻量对应用服务器消耗较小，虽然Logstash也可以采集数据，但Logstash占用应用服务器性能比Filebeat大

## springboot log框架包

* /**[logstash-logback-encoder](https://github.com/logstash/logstash-logback-encoder)** Star 1.7k
* /**[logback-kafka-appender](https://github.com/danielwegener/logback-kafka-appender)** Star 472
* /**[logback-more-appenders](https://github.com/sndyuk/logback-more-appenders)** Star 87
* [kmtong](https://github.com/kmtong)/**[logback-redis-appender](https://github.com/kmtong/logback-redis-appender)** Star 103

## 架构选型

### 方案一 EFK(docker log模式)

利用Filebeat采集docker日志，从而监控docker上所有或指定服务的日志，实现SpringCloud的日志监听

优点: 对现有服务侵入无，不需要改造现有服务

缺点：强依赖于docker，只能监听docker

```mermaid
graph LR
B(Filebeat收集docker日志)-->E[Elasticsearch]-->K[Kibana]
```

### 方案二  Logstash采用

优点：简洁，搭建快速

缺点：没缓冲，可能会有瓶颈

```mermaid
graph LR
B(Logstash收集本地log文件)-->E[Elasticsearch]-->K[Kibana]
```

### 方案三 Logstash+redis+Logstash(未验证)

参考：[搭建 ELK 实时日志平台并在 Spring Boot 和 Nginx 项目中使用](https://developer.ibm.com/zh/articles/build-elk-and-use-it-for-springboot-and-nginx/)

优点：

1. 直接读取日志文件，对原来的系统入侵无，
2. 支持所有服务，例如nginx,springboot等只要能生成日志文件的

缺点：

1. 需要在读取日志文件的服务器都安装Logstash(shipper角色)
2. 采用docker部署的时候，springboot需要映射日志目录

```mermaid
graph LR
B(Logstash收集本地log文件/Shipper)--写入-->G([redis])--读取-->L[Logstash/Indexer角色]-->E[Elasticsearch]-->K[Kibana]

```

### 方案四 kafka+logstash(未验证)

参考：[Spring Cloud集成ELK完成日志收集实战（elasticsearch、logstash、kibana](https://blog.csdn.net/zjx2016/article/details/104311744)

优点：

1. 不需要在应用服务器安装额外的服务
2. 支持docker部署，不需要额外映射服务目录

缺点：

1. 需要改造springboot
2. 不支持nginx、数据库等服务

```mermaid
graph LR
B(springboot)--写入-->G([kafka])--读取-->L[Logstash]-->E[Elasticsearch]-->K[Kibana]
```

### 方案五 EFK+[logback-more-appenders](https://github.com/sndyuk/logback-more-appenders)

参考：[sndyuk](https://github.com/sndyuk)/**[logback-more-appenders](https://github.com/sndyuk/logback-more-appenders)**

优点：

缺点：



## EFK/ELK部署

参考[deviantony/docker-elk](https://github.com/deviantony/docker-elk)

`docker-stack.yml`内容如下

```yaml
version: '3.3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.9.0
    configs:
      - source: elastic_config
        target: /usr/share/elasticsearch/config/elasticsearch.yml
    environment:
      ES_JAVA_OPTS: "-Xmx256m -Xms256m"
      ELASTIC_PASSWORD: changeme
      discovery.type: single-node
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.hostname == me]  
  logstash:
    image: docker.elastic.co/logstash/logstash:7.9.0
    configs:
      - source: logstash_config
        target: /usr/share/logstash/config/logstash.yml
      - source: logstash_pipeline
        target: /usr/share/logstash/pipeline/logstash.conf
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.hostname == me]        
  kibana:
    image: docker.elastic.co/kibana/kibana:7.9.0
    ports:
      - "14020:5601"
    configs:
      - source: kibana_config
        target: /usr/share/kibana/config/kibana.yml
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.hostname == me]     
  filebeat:
    image: docker.elastic.co/beats/filebeat:7.9.0
    user: root
    command: filebeat -e -strict.perms=false
    configs:
      - source: filebeat_config
        target: /usr/share/filebeat/filebeat.yml
    volumes:
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.hostname == me]           
configs:
  elastic_config:
    external: true
  logstash_config:
    external: true
  logstash_pipeline:
    external: true
  kibana_config:
    external: true
  filebeat_config:
    external: true
```

各个配置文件配置内容如下:

`elastic_config`

```yaml
---
## Default Elasticsearch configuration from Elasticsearch base image.
## https://github.com/elastic/elasticsearch/blob/master/distribution/docker/src/docker/config/elasticsearch.yml
#
cluster.name: "docker-cluster"
network.host: 0.0.0.0

## X-Pack settings
## see https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-xpack.html
#
xpack.license.self_generated.type: trial
xpack.security.enabled: true
xpack.monitoring.collection.enabled: true
```

`kibana_config`

```yaml
---
## Default Kibana configuration from Kibana base image.
## https://github.com/elastic/kibana/blob/master/src/dev/build/tasks/os_packages/docker_generator/templates/kibana_yml.template.js
#
server.name: kibana
server.host: 0.0.0.0
elasticsearch.hosts: [ "http://elasticsearch:9200" ]
monitoring.ui.container.elasticsearch.enabled: true

## X-Pack security credentials
#
elasticsearch.username: elastic
elasticsearch.password: changeme
```

` logstash_config`

```yaml
---
## Default Logstash configuration from Logstash base image.
## https://github.com/elastic/logstash/blob/master/docker/data/logstash/config/logstash-full.yml
#
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: [ "http://elasticsearch:9200" ]

## X-Pack security credentials
#
xpack.monitoring.enabled: true
xpack.monitoring.elasticsearch.username: elastic
xpack.monitoring.elasticsearch.password: changeme
```

`logstash_pipeline`

```yaml
input {
	tcp {
		port => 5000
	}
}

## Add your filters / logstash plugins configuration here

output {
	elasticsearch {
		hosts => "elasticsearch:9200"
		user => "elastic"
		password => "changeme"
	}
}
```

`filebeat_config`

```yaml
filebeat.config:
  modules:
    path: ${path.config}/modules.d/*.yml
    reload.enabled: false

filebeat.autodiscover:
  providers:
    - type: docker
      hints.enabled: true

processors:
- add_cloud_metadata: ~

output.elasticsearch:
  hosts: 'elasticsearch:9200'
  username: 'elastic'
  password: 'changeme'
```



