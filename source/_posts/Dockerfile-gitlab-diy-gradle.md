---
title: gitlab-runner镜像自定义
date: 2018-01-20 19:26:38
categories: Docker
tags: [Docker,gitlab,runner,Dockerfile]
---
## gitlab-runner镜像自定义

仓库[**DockerHub**](https://hub.docker.com/):[gitlab/gitlab-runner](https://hub.docker.com/r/gitlab/gitlab-runner/)

### gitlab版本

[gitlab-runner](https://gitlab.com/gitlab-org/gitlab-runner/tree/master/dockerfiles/ubuntu) (2018.1.16)

[gitlab-runner_amd64.deb](https://packages.gitlab.com/runner/gitlab-runner?filter=debs)

###### 准备工作

```sh
wget https://packages.gitlab.com/runner/gitlab-runner/packages/linuxmint/sonya/gitlab-runner_10.3.0_amd64.deb/download -O gitlab-runner_amd64.deb
#编译
sudo docker build -t xuan-runner:v1 .
```

```dockerfile
FROM ubuntu:14.04

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y ca-certificates wget apt-transport-https vim nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG DOCKER_MACHINE_VERSION=0.13.0
ARG DUMB_INIT_VERSION=1.0.2

COPY gitlab-runner_amd64.deb /tmp/
#COPY checksums /tmp/
#runner diy
COPY jdk1.8.0_161 /usr/lib/jvm/java-8-oracle
COPY gradle-4.4.1 /usr/lib/gradle

RUN dpkg -i /tmp/gitlab-runner_amd64.deb; \
    apt-get update &&  \
    apt-get -f install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/gitlab-runner_amd64.deb && \
    gitlab-runner --version && \
    mkdir -p /etc/gitlab-runner/certs && \
    chmod -R 700 /etc/gitlab-runner && \
    wget -q https://github.com/docker/machine/releases/download/v${DOCKER_MACHINE_VERSION}/docker-machine-Linux-x86_64 -O /usr/bin/docker-machine && \
    chmod +x /usr/bin/docker-machine && \
    docker-machine --version && \
    wget -q https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 -O /usr/bin/dumb-init && \
    chmod +x /usr/bin/dumb-init && \
    dumb-init --version 
    #&& \
 #   sha256sum --check --strict /tmp/checksums
ENV J2SDKDIR /usr/lib/jvm/java-8-oracle
ENV J2REDIR /usr/lib/jvm/java-8-oracle/jre
ENV PATH $PATH:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV DERBY_HOME /usr/lib/jvm/java-8-oracle/db
ENV GRADLE_HOME /usr/lib/gradle 
ENV PATH $GRADLE_HOME/bin:$PATH

COPY entrypoint /
RUN chmod +x /entrypoint

VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]
ENTRYPOINT ["/usr/bin/dumb-init", "/entrypoint"]
CMD ["run", "--user=gitlab-runner", "--working-directory=/home/gitlab-runner"]
```

```shell
#!/bin/bash

# gitlab-runner data directory
DATA_DIR="/etc/gitlab-runner"
CONFIG_FILE=${CONFIG_FILE:-$DATA_DIR/config.toml}
# custom certificate authority path
CA_CERTIFICATES_PATH=${CA_CERTIFICATES_PATH:-$DATA_DIR/certs/ca.crt}
LOCAL_CA_PATH="/usr/local/share/ca-certificates/ca.crt"

update_ca() {
  echo "Updating CA certificates..."
  cp "${CA_CERTIFICATES_PATH}" "${LOCAL_CA_PATH}"
  update-ca-certificates --fresh >/dev/null
}

if [ -f "${CA_CERTIFICATES_PATH}" ]; then
  # update the ca if the custom ca is different than the current
  cmp --silent "${CA_CERTIFICATES_PATH}" "${LOCAL_CA_PATH}" || update_ca
fi

# launch gitlab-runner passing all arguments
exec gitlab-runner "$@"
```



### dockerhub版本（废弃）

原因：该版本安装的是gitlab-ci-multi-runner是之前的版本现在已更名为gitlab-runner，而且运行报错

`[dumb-init] /entrypoint: Exec format error`，以为是最后句名字报错，但是修改报同样的错

[ayufan/gitlab-ci-multi-runner](https://github.com/ayufan/gitlab-ci-multi-runner/tree/master/dockerfiles/ubuntu) (2016.5月更新)

```dockerfile
#--file name--Dockerfile---
#指定基础镜像
FROM ubuntu:14.04

#远程拷贝文件到指定目录，带自动解压功能
ADD https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64 /usr/bin/dumb-init
RUN chmod +x /usr/bin/dumb-init

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y ca-certificates wget apt-transport-https vim nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "deb https://packages.gitlab.com/runner/gitlab-ci-multi-runner/ubuntu/ `lsb_release -cs` main" > /etc/apt/sources.list.d/runner_gitlab-ci-multi-runner.list && \
    wget -q -O - https://packages.gitlab.com/gpg.key | apt-key add - && \
    apt-get update -y && \
    apt-get install -y gitlab-ci-multi-runner && \
    wget -q https://github.com/docker/machine/releases/download/v0.7.0/docker-machine-Linux-x86_64 -O /usr/bin/docker-machine && \
    chmod +x /usr/bin/docker-machine && \
    apt-get clean && \
    mkdir -p /etc/gitlab-runner/certs && \
    chmod -R 700 /etc/gitlab-runner && \
    rm -rf /var/lib/apt/lists/*

ADD entrypoint /
RUN chmod +x /entrypoint
#匿名卷，如果运行时没有指定卷则自动创建匿名卷
VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]
#应用运行前执行的脚本
ENTRYPOINT ["/usr/bin/dumb-init", "/entrypoint"]
#启动容器前执行的命令
CMD ["run", "--user=gitlab-runner", "--working-directory=/home/gitlab-runner"]
```

```shell
#--file name--entrypoint---
#!/bin/bash

# gitlab-ci-multi-runner data directory
DATA_DIR="/etc/gitlab-runner"
CONFIG_FILE=${CONFIG_FILE:-$DATA_DIR/config.toml}
# custom certificate authority path
CA_CERTIFICATES_PATH=${CA_CERTIFICATES_PATH:-$DATA_DIR/certs/ca.crt}
LOCAL_CA_PATH="/usr/local/share/ca-certificates/ca.crt"

update_ca() {
  echo "Updating CA certificates..."
  cp "${CA_CERTIFICATES_PATH}" "${LOCAL_CA_PATH}"
  update-ca-certificates --fresh >/dev/null
}

if [ -f "${CA_CERTIFICATES_PATH}" ]; then
  # update the ca if the custom ca is different than the current
  cmp --silent "${CA_CERTIFICATES_PATH}" "${LOCAL_CA_PATH}" || update_ca
fi

# launch gitlab-ci-multi-runner passing all arguments
#这句报错，版本问题，似乎是multi-runner是之前的版本，先更新为gtilab-runner
#exec gitlab-ci-multi-runner "$@" ,
exec gitlab-runner "$@"
```

