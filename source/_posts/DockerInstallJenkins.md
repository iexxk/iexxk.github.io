---
title: Docker-Install-Jenkins
date: 2018-05-21 19:04:52
updated: 2019-02-18 11:17:11
categories: Docker
tags: [Docker,Jenkins]
---

## 简介

github文档：[jenkinsci/docker](https://github.com/jenkinsci/docker/blob/master/README.md)

[jenkins官网](https://jenkins.io/)

Docker hub：[jenkins/jenkins](https://hub.docker.com/r/jenkins/jenkins/)

[蓝色主题版](https://jenkins.io/doc/book/blueocean/getting-started/):[jenkinsci/blueocean](https://hub.docker.com/r/jenkinsci/blueocean/)



## 安装

脚本文件https://github.com/xuanfong1/config/blob/master/dockerStack/stack-jenkins.yml

创建挂载目录

启动提示：

```verilog
touch: cannot touch '/var/jenkins_home/copy_reference_file.log': Permission denied

Can not write to /var/jenkins_home/copy_reference_file.log. Wrong volume permissions?
```

解决：执行`chown -R 1000:1000 /dockerdata/v-jenkins/jenkins_home`改变用户组为1000 用户1000



### jenkins 之docker插件

[docker-build-step](https://plugins.jenkins.io/docker-build-step) 构建步骤使用docker命令

[CloudBees Docker Build and Publish](https://plugins.jenkins.io/docker-build-publish)镜像构建以及推送仓库

[Docker](https://plugins.jenkins.io/docker-plugin) 远程连接docker进行代理构建

[Docker API](https://plugins.jenkins.io/docker-java-api)提供其他插件docker服务api

[CloudBees Docker Custom Build Environment](https://plugins.jenkins.io/docker-custom-build-environment)构建镜像或从仓库拉去镜像

[Docker Swarm](https://plugins.jenkins.io/docker-swarm)集群



https://github.com/boxboat/jenkins-demo



错误处理

1. 连接错误，解决添加挂在卷`"/var/run/docker.sock:/var/run/docker.sock" `

   ```verilog
   Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
   
   script returned exit code 1
   ```

2. 连接没权限,解决

   ```
   Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.35/build?buildargs=%7B%7D&cachefrom=%5B%5D&cgroupparent=&cpuperiod=0&cpuquota=0&cpusetcpus=&cpusetmems=&cpushares=0&dockerfile=Dockerfile&labels=%7B%7D&memory=0&memswap=0&networkmode=default&rm=1&session=6ec5bc5a7afd427649abb0a03b733c9586dd9271474c89359e31a3910ed971e8&shmsize=0&t=e5e2d0e18760db6972a9c42a9a81653e633ff131&target=&ulimits=null: dial unix /var/run/docker.sock: connect: permission denied
   
   script returned exit code 1
   ```

   执行`sudo ls -la /var/run/docker.sock `

   ```
   srw-rw----. 1 root docker 0 5月  15 16:36 /var/run/docker.sock
   ```

   `--group-add=$(stat -c %g /var/run/docker.sock)`

   `sudo usermod -a -G docker jenkins`

   解决方案

   ##### 方案一

   改变socke所属的用户组

   用root用户进入jenkins容器

   执行`chown :jenkins /var/run/docker.sock`

   ```powershell
   -------------宿主机------------------------------
   [root@worker ~]# ls -la /var/run/docker.sock
   srw-rw----. 1 root docker 0 6月   6 16:58 /var/run/docker.sock
   执行后
   [root@worker ~]# ls -la /var/run/docker.sock
   srw-rw----. 1 root 1000 0 6月   6 16:58 /var/run/docker.sock
   ------------------jenkins容器---------------------
   srw-rw---- 1 root 994 0 Jun  6 08:58 var/run/docker.sock
   执行后
   srw-rw---- 1 root jenkins 0 Jun  6 08:58 var/run/docker.sock
   ```

   `cat /etc/group`查看用户组id

   自我理解：

   这里通过挂载卷的形式共享/var/run/docker.sock套接字，但是默认套接字属于root docker组，这里docker的组id为994，但是容器内没有994的组，所以直接显示994，最后执行这个`chown :jenkins /var/run/docker.sock`之后把组更改为乐jenkins组，但是默认宿主机是没有jenkins组，所以直接显示jenkins的id 1000，这里直接修改为jenkins用户组，虽然可以解决权限问题，不知道会不会影响其他的使用该sock套接字（**隐患**）

   完善思路：

   新建个jenkins组

   添加docker用户到jenkins组

   但是发现

   宿主机`id docker` 没有docker用户

   且docker组没有任何用户，因此可以放心更改组，所以要不要新建组待考虑

   ```shell
   cat /etc/group #查看组信息
   cgred:x:995:
   docker:x:994:jenkins
   #组名:口令(默认空/*):组标识号(gid):组内用户列表
   ```

   ##### 方案二

   自我新思路

   宿主机创建个jenkins用户组指定id1000

   宿主机执行`useradd -u 1000 jenkins`

   然后执行`sudo usermod -a -G docker jenkins`

   失败，没有权限

   ##### 方案三(未实验)

   root用户可以访问docker,需要重写dockerfile

   ```
   FROM <base-image>
   USER root
   ```

   隐患：不知到用root用户登陆会不会影响jenkins的一些功能

   ##### 方案四(未实验)

   修改`groupadd -g 994 docker`，找不到命令

   然后执行`usermod -a -G docker jenkins`

   此法每次重启容器都会丢失配置，虽然可以通过挂载目录形式保存设置，太麻烦。

3. Jenkins 第一次打开，一直显示启动中

   解决：

   修改jenkins_home/updates/default.json

   把 "connectionCheckUrl":"http://www.google.com/" 改为 "connectionCheckUrl":"http://www.baidu.com/"

   https://github.com/jenkinsci/docker/issues/263



## centos 安装jenkins,需要jdk8

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install jenkins
sudo service jenkins start/stop/restart
sudo chkconfig jenkins on
```

