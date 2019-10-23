---
title: Dcoker-gitlab-ci
date: 2019-10-15 23:43:21
updated: 2019-10-16 10:37:59
categories: Docker
tags: [Docker,gitlab]
---

## gitlab-ci构建docker镜像的三种方式

[官方教程](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html)

### shell模式（dood），自定义runner镜像

见: [Docker-Gitlab-Runner](https://blog.iexxk.com/2018/07/31/docker-gitlab-runner/)

优点：

1. 自定义镜像，集成自己需要的工具

缺点：

1. 采用宿主机docker进行编译

### docker模式（dind），采用docker内部docker

[Docker in Docker 19.03 service fails](https://gitlab.com/gitlab-org/gitlab-runner/issues/4501)

优点:

1. 独立(不影响宿主机)，可以多线程构建

缺点:

1. 需要`vi /etc/gitlab-runner/config.toml`设置`[runners.docker]->privileged = true`特权模式
2. 编译慢每次要启动docker服务

版本19以后tls需要挂载或者禁用

```yaml
#[三种方式使用docker构建](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html)
#如果stages没有设置镜像，就使用该镜像
image: docker:19.03.1

# docker in docker =docker dind 容器内部启动docker
# docker out docker = dood 使用宿主机的docker，需要挂在/var/run/docker.sock
services:
  - name: docker:19.03.1-dind

#docker in docker 版本19之后要禁用tls，后者配置证书
variables:
  DOCKER_TLS_CERTDIR: ""


#每一个stages都会git clone项目
stages:
  - package
  - build
  - deploy

#每一个stages前都会执行这下面的脚本
before_script:
  - pwd
  - ls

gradle_package:
  image: java:8
  stage: package
  only:
    - deploy-dev
  script:
    - ./gradlew bootJar
  artifacts:
    paths:
      - build/libs/
docker_build:
  stage: build
  only:
    - deploy-dev
  script:
    - docker build -t test:latest .
```

### docker模式(dood)

