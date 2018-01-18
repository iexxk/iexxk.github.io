---
title: Docker swarm搭建总结
date: 2017-12-05 16:12:37
categories: Docker
tags: [集群,Swarm,Docker]
---

#### 安装

[Get Docker CE for Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)

```sh
#查看可安装版本
apt-cache madison docker-ce
#安装指定版本(降级)
sudo apt install docker-ce=17.09.1~ce-0~ubuntu
```

1. `docker-ce | 17.12.0~ce-0~ubuntu` 安装gitlab出现 `Failed to find a load balance…` 错误

   解决降级版本17.09.1解决


#### 挂载卷Volume与Bind

##### Volume 数据卷

会把container的一个目录映射到一个数据卷，一个目录只能映射一个数据卷，不需要新建目录

```mermaid
graph LR
A[containner目录] --> |映射| B[数据卷]
```

##### Bind 绑定本地目录

container的一个目录会加载本地目录，因此需要在本地提前新建该目录，不然启动会找不到目录

```mermaid
graph LR
A[本地目录] --> |指向| B[containner目录]
```



