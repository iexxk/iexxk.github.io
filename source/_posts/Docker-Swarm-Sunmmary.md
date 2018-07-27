---
title: Docker swarm搭建总结
date: 2017-12-05 16:12:37
updated: 2018-07-26 09:12:00
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

##### 方案选型与测试

方案有

- Flannel

- Open vSwitch

  http://dockone.io/article/228

- Weave

- pipework

- libnetwork

  [Docker Libnetwork 使用](http://dockone.io/article/1100)

- 动态路由

  [一条命令取代etcd+flannel，全网贯通无需端口映射](http://dockone.io/article/466)

####  [启动顺序](https://docs.docker.com/compose/startup-order/)

[[vishnubob]/**wait-for-it

#### entrypoint vs cmd

entrypoint 必须执行服务话

cmd 命令型，可执行

总结：

1. 如果用[wait-for](https://github.com/eficode/wait-for)支持alpine,使用sh，[wait-for-it](https://github.com/vishnubob/wait-for-it)使用bash
2. dockercompose会覆盖dockerfile里面的cmd命令
3. 通过挂载形式把脚本放进去执行，或者通过dockerfile 构建时构建进去
4. 在容器内进行测试时，发现不能跟/actuator/health，会连接超时，
5. 直接执行时,如果服务没启动也会超时，但是可以跟可以跟参数`-t`设置为0不超时，会一直等待

```yaml
#不能加/actuator/health，请求超时，不能用wait-for-it.sh  ,不支持alpine ，经测试感觉怪，还使用 depends_on
    command: ["./wait-for.sh", "config-server:14030", "--", "java","-jar","app.jar"]
    depends_on:
     - config-server
```

### 镜像升级

portainer升级命令

`docker service update --image portainer/portainer:latest portainer_portainer`

然后重启portainer服务

