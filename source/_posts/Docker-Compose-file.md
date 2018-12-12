---
title: Docker-Compose-file
date: 2018-04-28 09:36:44
updated: 2018-04-28 09:36:44
categories: Docker
tags: [Docker,stack,yaml,Compose]
---

## Compos file 版本3以上

[Compos file v3官网](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix)

#### [build](单机模式)

只支持单机运行

```yaml
version: "3" #指明版本3，docker stack需要版本3以上
services:
  webapp: 
    build:  #集群部署会忽略构建镜像，stack只支持提前构建好镜像
      context: ./dir #构建上下文路径
      dockerfile: Dockerfile-alternate  #构建文件
      args:  #构建参数
        buildno: 1
```

#### [configs](https://docs.docker.com/engine/swarm/configs/#simple-example-get-started-with-configs) (swarm模式)

只支持集群模式运行

```yaml
version: "3.3"
services:
  redis:
    image: redis:latest
    deploy:
      replicas: 1
    configs:
      - my_config
      - my_other_config
configs:
  my_config:
    file: ./my_config.txt
  my_other_config:
    external: true
```

#### [command]()

会覆盖dockerfile里面的命令例如：

```yaml
command: bundle exec thin -p 3000 #docker-compose.yml覆盖dockerfile的命令
command: ["bundle", "exec", "thin", "-p", "3000"] #dockerfile等效于上面的命令
```

#### deploy(swarm模式)

```yaml
version: '3.2'
services:
  redis:
    image: redis:alpine
    labels: #容器上的标签
       com.example.description: " containers 上的标签"
    deploy:
      mode: global #可选global(全局模式，每台机一个)/replicated(多台)
      replicas: 6 #部署的总数量
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
      endpoint_mode: vip  #可选vip(默认)/dnsrr，主要是IP啥的
      labels: #服务器上的标签
        com.example.description: "This label will appear on the web service"
      placement: #指定部署的信息
        constraints:
          - node.role == manager #只在管理节点运行
          - engine.labels.operatingsystem == ubuntu 14.04
        preferences:
          - spread: node.labels.zone
      resources: #资源限制
        limits:
          cpus: '0.50'
          memory: 50M
        reservations:
          cpus: '0.25'
          memory: 20M
      restart_policy: #重启策略
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      update_config: #更新配置策略
        parallelism: 2
        delay: 10s
        order: stop-first
    depends_on:  #依赖的服务模块，在db启动才启动服务，但是不能保证db启动完，如果要设置启动顺序见
    #https://docs.docker.com/compose/startup-order/
      - db
      - redis
    healthcheck: #健康检查
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 1m30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging: #日志服务
      driver: syslog
      options:
        syslog-address: "tcp://192.168.0.42:123"
    volumes: #自定义挂在卷
      - type: volume
      source: mydata
      target: /data
      volume:
      nocopy: true
      - type: bind
      source: ./static
      target: /opt/app/static
    ports:  #自定义端口
      - target: 80
        published: 8080
        protocol: tcp
        mode: host
```



### 问题

错误`services.nginx.ports.0 must be a string or number`是因为自定义端口,只支持3.2以上

```yaml
   version: '3.2' 
    ports:  #自定义端口
      - target: 80
        published: 8080
        protocol: tcp
        mode: host
```





