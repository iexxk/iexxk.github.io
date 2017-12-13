---
title: Docker集群之Swarm网络测试
date: 2017-09-19 17:27:37
categories: Docker
tags: [集群,Swarm,docker,nginx,overlay,ingress]
---
### Swarm 网络连通测试

##### 环境

* docker for  windos 17.06.2(10.0.75.1)
* centos7.3 docker

##### 测试

```shell
#manager>创建overlay网络
docker network create --driver overlay --subnet 10.0.9.0/24 my-network
#查看网络
docker network ls
#manager>创建nginx
docker service create --replicas 2 --name my-web --network my-network nginx
#查看my-web服务
docker service ps my-web
#查看my-network网络详情
docker network inspect my-network
#manager>创建busybox工具箱
docker service create --name my-busybox --network my-network busybox sleep 3000
#查看工具箱在那个节点
docker service ps my-busybox
#去工具箱的节点
 docker ps
#进入工具箱
 docker exec -it <工具箱的di or name> /bin/sh
#从busybox容器内部，查询DNS来查看my-web的VIP
nslookup my-web
#从busybox容器内部，使用特殊查询查询DNS，来找到my-web服务的所有容器的IP地址：
nslookup tasks.my-web
#从busybox容器内部，通过wget来访问my-web服务中运行的nginx网页服务器
wget -O- my-web
#增加实例
docker service update my-busybox --replicas 2
```

#### 参考

[基于Swarm的多主机容器网络](https://andyyoung01.github.io/2016/11/26/%E5%9F%BA%E4%BA%8ESwarm%E7%9A%84%E5%A4%9A%E4%B8%BB%E6%9C%BA%E5%AE%B9%E5%99%A8%E7%BD%91%E7%BB%9C/)

[官网](https://docs.docker.com/engine/swarm/ingress/)