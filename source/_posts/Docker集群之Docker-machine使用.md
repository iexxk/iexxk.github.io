---
title: Docker集群之Docker-machine使用
date: 2017-10-10 10:25:37
categories: docker集群
tags: [集群,Swarm,docker,nginx,overlay,ingress]
---
### Docker-machine

安装 [Docker Toolbox](https://www.docker.com/docker-toolbox)

官网：[docker/machine](https://github.com/docker/machine)

```powershell
#创建manager docker主机
docker-machine create -d hyperv manager
#查看主机
docker-machine ls
#删除主机
docker-machine rm -f manager
#进入docker主机
docker-machine ssh manager
#退出主机
exit
    docker swarm join --token SWMTKN-1-2483wscrxzqlzn1ulk8o3izurjqdzcrg38uihaontlll788mq5-d55xj8yaycb2392q5kv02v4kq 192.168.100.214:2377
```

