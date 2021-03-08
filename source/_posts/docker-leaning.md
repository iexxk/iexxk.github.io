---
title: docker入门学习
date: 2020-11-30 10:44:15
updated: 2021-03-05 16:35:36
categories: Docker
tags: [Docker]
---

# docker 名词解释

下面简单解释下名词的含义，后面会详细介绍：

* docker：docker代表这一个技术的名词，下面**一个docker**代表一台机器上装的一个docker服务
* container：docker容器，相当于一个轻量的沙盒系统（可以暂时理解一个运行好的虚拟机系统）一个容器只运行一个服务
* images：docker镜像，相当于一个安装包（可以暂时理解成一个系统iso镜像）
* service：docker服务，多个相同的容器组成的一个服务，相当于容器的多个复制，提高了扩展性
* swarm：docker集群，将一个docker或多个docker组成的一个资源集合，包含了网络、负载均衡、多个服务节点、服务发现、服务伸缩
* node：docker节点，一台实际机器上的一个docker算一个节点，节点只有在docker初始化为集群才存在该概念
* docker-compose.yml：服务编排脚本，该脚本只支持单机docker服务编排，相当于服务的启动参数，服务数量都在该脚本配置
* stack：docker集群服务编排模式,stack.yml为集群部署模式的配置文件，文件name可以自定义，这个是多节点服务编排部署模式，在单机的基础上面多支持了容器在那个节点运行，及运行个数等
* DockerFile：docker镜像编排脚本
* [Docker-hub](https://hub.docker.com/search?q=&type=image)：官方docker仓库
* registry：可搭建的私有镜像仓库
* 集群-无状态服务vs有状态服务(共享存储/NAS)
* 分布式集群

docker swarm服务关系

[![6VVz11.png](https://s3.ax1x.com/2021/03/04/6VVz11.png)](https://imgtu.com/i/6VVz11)

docker编排部署流程

[![6VZP0O.png](https://s3.ax1x.com/2021/03/04/6VZP0O.png)](https://imgtu.com/i/6VZP0O)

# [docker简介](https://www.docker.com/resources/what-container)

容器是打包代码及其所有依赖项的软件的标准单元，因此应用程序可以从一个计算环境快速可靠地运行到另一个计算环境。Docker容器映像是一个轻量级的，独立的，可执行的软件软件包，其中包含运行应用程序所需的一切：代码，运行时，系统工具，系统库和设置。

#### 优势：

- **标准：** Docker创建了容器的行业标准，因此它们可以在任何地方移植
- **轻巧：**容器共享计算机的OS系统内核，因此不需要每个应用程序都具有OS，从而提高了服务器效率，并降低了服务器和许可成本
- **安全：**容器中的应用程序更安全，Docker提供业界最强大的默认隔离功能

#### 虚机vs容器

容器虚化的是操作系统而不是硬件，容器更加便携和高效

[![6VJ3LQ.png](https://s3.ax1x.com/2021/03/04/6VJ3LQ.png)](https://imgtu.com/i/6VJ3LQ)

# [docker安装部署](https://blog.iexxk.com/2017/10/10/docker-install-base/?highlight=docker)

#### [centos安装](https://docs.docker.com/engine/install/centos/)

```bash
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
#启动
systemctl start docker.service
# 开机启动
systemctl enable docker
```

#### [docker swarm 初始化](https://blog.iexxk.com/2017/09/14/docker-install-swarm/?highlight=docker+swarm)

# [DockerFile镜像编排](https://docs.docker.com/engine/reference/builder/)

```bash
# 镜像编排命令
docker build -t image-name:tag .
```

dockerfile常见命令说明

```dockerfile
#基础镜像选择alpine 小巧安全流行方便
FROM exxk/tomcat:8-alpine-cst-font
#指定用户
USER patrick
#指定工作目录
WORKDIR /path/to/workdir
#编译时的环境参数
ARG DOCKER_MACHINE_VERSION
#暴露的端口
EXPOSE 80/udp
#拷贝文件到镜像的指定目录
COPY geoserver /usr/local/tomcat/webapps/geoserver
#拷贝文件，但是add功能比copy多，压缩文件会自动解压，不建议用高级的add
ADD geoserver /usr/local/tomcat/webapps/geoserver
#设置环境变量，启动时可以通过参数进行覆盖
ENV GEOSERVER_HOME=/usr/local/tomcat/webapps/geoserver/data
#运行编译时的命令
RUN chmod +x /usr/bin/gitlab-runner
#健康检查/类似心跳，前面命令执行的时间，cmd后面为心跳检测的命令
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1
#设置挂在卷
VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]
#启动时容器时，初始化容器的命令脚本
ENTRYPOINT ["/usr/bin/dumb-init", "/entrypoint"]
#入口启动命令
CMD ["catalina.sh", "run"]
```

## [Docker-hub](https://hub.docker.com/?ref=login) 和 [registry](https://blog.iexxk.com/2018/01/24/docker-install-registry/?highlight=regis)



# [docker-compose](https://blog.iexxk.com/2018/04/28/docker-compose-file/?highlight=compose)

[官方文档](https://docs.docker.com/compose/compose-file/)

# [docker swarm](https://blog.iexxk.com/2017/09/14/docker-install-swarm/?highlight=swarm) VS k8s(Kubernetes)

[![6eAkhd.jpg](https://s3.ax1x.com/2021/03/05/6eAkhd.jpg)](https://imgtu.com/i/6eAkhd)



## 平台安装部署流程

[![6e1abd.png](https://s3.ax1x.com/2021/03/05/6e1abd.png)](https://imgtu.com/i/6e1abd)

[![6e1UDH.png](https://s3.ax1x.com/2021/03/05/6e1UDH.png)](https://imgtu.com/i/6e1UDH)

[![6e1NKe.png](https://s3.ax1x.com/2021/03/05/6e1NKe.png)](https://imgtu.com/i/6e1NKe)





## springboot和docker 环境变量

springboot 支持系统环境变量
docker 支持容器环境变量设置

设计原理，不改变基础镜像的情况下，适应不同的环境

```bash
优先级由高到低
1	启动命令中指定的配置项；
2	操作系统配置项；
3	环境变量
4	配置中心中的配置文件；
5	本地的application.properties(yml)
5	本地boostrap.properties（yml）
```
[![6eGvIs.png](https://s3.ax1x.com/2021/03/05/6eGvIs.png)](https://imgtu.com/i/6eGvIs)

