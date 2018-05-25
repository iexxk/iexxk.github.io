---
title: Docker-Install-Jenkins
date: 2018-05-21 19:04:52
updated: 2018-05-21 19:04:52
categories: Docker
tags: [Docker,Jenkins]
---

## 简介

github文档：[jenkinsci/docker](https://github.com/jenkinsci/docker/blob/master/README.md)

[jenkins官网](https://jenkins.io/)

Docker hub：[jenkins/jenkins](https://hub.docker.com/r/jenkins/jenkins/)

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

