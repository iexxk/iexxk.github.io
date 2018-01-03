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

