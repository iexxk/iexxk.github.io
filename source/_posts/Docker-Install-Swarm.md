---
title: Docker集群之安装Swarm
date: 2017-09-14 10:07:37
updated: 2018-04-25 20:47:32categories: Docker
tags: [集群,Swarm,Docker]
---
### [Docker Swarm](https://docs.docker.com/engine/swarm/)官网

### 准备工作

```powershell
#centos7.3
Docker version 17.06.2-ce, build cec0b72
#win10
Docker version 17.06.2-ce, build cec0b72
```

* TCP 2377 集群管理通信
* TCP/UDP 7946 容器(container)网络发现
* UDP 4789 容器(container)入口网络

## Swarm 安装

centos manager(xuanPs)

```sh
#初始化节点
docker swarm init --advertise-addr 112.74.51.136
#echo输出如下内容，在work节点执行改命令加入改manger(windos执行)
docker swarm join --token SWMTKN-1-34egnv0ksgzg6enh47wmze0ncx90bo2218yaetm88p6s028i2s-c46n408x51lklv1n3myhmpt1a 112.74.51.136:2377
#查看节点
docker node ls
```

#### 创建和删除服务

###### 参考[inspect-service](https://docs.docker.com/engine/swarm/swarm-tutorial/inspect-service/)、[scale-service](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/)、[delete-service](https://docs.docker.com/engine/swarm/swarm-tutorial/delete-service/)

`docker service create --replicas 1 --name helloworld alpine ping docker.com`

* `docker service create` 创建服务
* `--name` 服务的名字
* `--replicas` 指定实例运行数量
* `alpine ping docker.com`指定alpine执行ping命令

```sh
#查看运行的服务
docker service ls
#查看某服务状态
docker service ps <服务名>
#运行5个helloworld服务
docker service scale helloworld=5
#移除helloworld服务
docker service rm helloworld
#检查helloworld是否存在
docker service inspect helloworld
```

#### 升级服务

`docker service create --replicas 3 --name redis --update-delay 10s redis:3.0.6`

* `--update-delay`多个服务启动时之间的时间间隔eg:`4h2m1s`

###### 参考[rolling-update](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/)

```powershell
#创建运行rdeis3.0.6服务
docker service create --replicas 3 --name redis --update-delay 10s redis:3.0.6
#查看redis images版本为3.0.6
docker service inspect --pretty redis
#更新redis镜像到3.0.7
docker service update --image redis:3.0.7 redis
#更新redis服务为最新镜像
docker service update --detach=false redis
#查看是否为3.0.7
docker service ps redis
```

#### 关闭一个节点

###### 参考[drain-node](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/)

```powershell
#关闭moby节点Availability为drain
docker node update --availability drain moby
#查看rdeis服务还是三个只不过在其他机器上
docker service ps redis
#查看moby节点状态
docker node inspect --pretty moby
#开启moby节点
docker node update --availability active moby
```

#### 使用群组路由模式

###### 参考[Use swarm mode routing mesh](https://docs.docker.com/engine/swarm/ingress/)

  ```json
{
  "registry-mirrors": ["https://rq98iipq.mirror.aliyuncs.com"]
}
  ```
