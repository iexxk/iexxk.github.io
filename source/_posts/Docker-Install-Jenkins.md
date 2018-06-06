---
title: Docker-Install-Jenkins
date: 2018-05-21 19:04:52
updated: 2018-06-06 14:01:34
categories: Docker
tags: [Docker,Jenkins]
---

## 简介

github文档：[jenkinsci/docker](https://github.com/jenkinsci/docker/blob/master/README.md)

[jenkins官网](https://jenkins.io/)

Docker hub：[jenkins/jenkins](https://hub.docker.com/r/jenkins/jenkins/)

[绿色主题版](https://jenkins.io/doc/book/blueocean/getting-started/):[jenkinsci/blueocean](https://hub.docker.com/r/jenkinsci/blueocean/)



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

https://github.com/jenkinsci/docker/issues/263

