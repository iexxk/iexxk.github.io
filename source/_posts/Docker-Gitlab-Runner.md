---
title: Docker-Gitlab-Runner
date: 2018-07-31 18:25:16
updated: 2018-08-03 17:53:58
categories: Docker
tags: [Docker,Gitlab,CI]
---

### 自定义镜像

#### docker [alpine-docker-cli镜像](https://github.com/nathanielc/docker-client)

```dockerfile
FROM gitlab/gitlab-runner:alpine
RUN apk add --no-cache curl

ENV VERSION "18.06.0-ce"
RUN curl -L -o /tmp/docker-$VERSION.tgz https://download.docker.com/linux/static/stable/x86_64/docker-$VERSION.tgz \
    && tar -xz -C /tmp -f /tmp/docker-$VERSION.tgz \
    && mv /tmp/docker/docker /usr/bin \
```

#### [gitlab-runner](https://gitlab.com/gitlab-org/gitlab-runner/tree/master/dockerfiles/alpine)

```dockerfile
FROM alpine:3.7

RUN adduser -D -S -h /home/gitlab-runner gitlab-runner

RUN apk add --update \
    bash \
    ca-certificates \
    git \
    openssl \
    tzdata \
    wget

ARG DOCKER_MACHINE_VERSION
ARG DUMB_INIT_VERSION

COPY gitlab-runner-linux-amd64 /usr/bin/gitlab-runner
COPY checksums /tmp/
RUN chmod +x /usr/bin/gitlab-runner && \
    ln -s /usr/bin/gitlab-runner /usr/bin/gitlab-ci-multi-runner && \
    gitlab-runner --version && \
    mkdir -p /etc/gitlab-runner/certs && \
    chmod -R 700 /etc/gitlab-runner && \
    wget -q https://github.com/docker/machine/releases/download/v${DOCKER_MACHINE_VERSION}/docker-machine-Linux-x86_64 -O /usr/bin/docker-machine && \
    chmod +x /usr/bin/docker-machine && \
    docker-machine --version && \
    wget -q https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 -O /usr/bin/dumb-init && \
    chmod +x /usr/bin/dumb-init && \
    dumb-init --version && \
    sha256sum -c -w /tmp/checksums

COPY entrypoint /
RUN chmod +x /entrypoint

VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]
ENTRYPOINT ["/usr/bin/dumb-init", "/entrypoint"]
CMD ["run", "--user=gitlab-runner", "--working-directory=/home/gitlab-runner"]
```

#### [maven](https://github.com/carlossg/docker-maven/tree/master/jdk-8-alpine)

```dockerfile
FROM openjdk:8-jdk-alpine

RUN apk add --no-cache curl tar bash procps

ARG MAVEN_VERSION=3.5.4
ARG USER_HOME_DIR="/root"
ARG SHA=ce50b1c91364cb77efe3776f756a6d92b76d9038b0a0782f7d53acf1e997a14d
ARG BASE_URL=https://apache.osuosl.org/maven/maven-3/${MAVEN_VERSION}/binaries

RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
  && curl -fsSL -o /tmp/apache-maven.tar.gz ${BASE_URL}/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && echo "${SHA}  /tmp/apache-maven.tar.gz" | sha256sum -c - \
  && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
  && rm -f /tmp/apache-maven.tar.gz \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn

ENV MAVEN_HOME /usr/share/maven
ENV MAVEN_CONFIG "$USER_HOME_DIR/.m2"

COPY mvn-entrypoint.sh /usr/local/bin/mvn-entrypoint.sh
COPY settings-docker.xml /usr/share/maven/ref/

ENTRYPOINT ["/usr/local/bin/mvn-entrypoint.sh"]
CMD ["mvn"]
```

#### [java](https://github.com/docker-library/openjdk/tree/master/8/jdk/alpine)

```dockerfile
#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM alpine:3.8

# A few reasons for installing distribution-provided OpenJDK:
#
#  1. Oracle.  Licensing prevents us from redistributing the official JDK.
#
#  2. Compiling OpenJDK also requires the JDK to be installed, and it gets
#     really hairy.
#
#     For some sample build times, see Debian's buildd logs:
#       https://buildd.debian.org/status/logs.php?pkg=openjdk-8

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home
ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

ENV JAVA_VERSION 8u171
ENV JAVA_ALPINE_VERSION 8.171.11-r0

RUN set -x \
	&& apk add --no-cache \
		openjdk8="$JAVA_ALPINE_VERSION" \
	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]

# If you're reading this and have any feedback on how this image could be
# improved, please open an issue or a pull request so we can discuss it!
#
#   https://github.com/docker-library/openjdk/issues
```



#### gitrunner+docker+ jdk+maven+npm(采用)

```dockerfile
FROM gitlab/gitlab-runner:alpine
# 公共需求+npm安装（nodejs nodejs-npm）(shadow 是 权限usermod修改)
RUN echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories \ 
&& apk add --no-cache curl tar bash procps nodejs nodejs-npm shadow \
&& npm install -g cnpm --registry=https://registry.npm.taobao.org
# docker
ENV VERSION "18.06.0-ce"
RUN curl -L -o /tmp/docker-$VERSION.tgz https://download.docker.com/linux/static/stable/x86_64/docker-$VERSION.tgz \
    && tar -xz -C /tmp -f /tmp/docker-$VERSION.tgz \
    && mv /tmp/docker/docker /usr/bin \
    && rm -rf /tmp/docker-$VERSION.tgz /tmp/docker \
    && usermod -g root gitlab-runner

# java
ENV LANG C.UTF-8

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home
ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

ENV JAVA_VERSION 8u171
ENV JAVA_ALPINE_VERSION 8.171.11-r0

RUN set -x \
	&& apk add --no-cache \
		openjdk8="$JAVA_ALPINE_VERSION" \
	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]

# maven

ARG MAVEN_VERSION=3.5.4
ARG USER_HOME_DIR="/root"
ARG SHA=ce50b1c91364cb77efe3776f756a6d92b76d9038b0a0782f7d53acf1e997a14d
ARG BASE_URL=https://apache.osuosl.org/maven/maven-3/${MAVEN_VERSION}/binaries

RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
  && curl -fsSL -o /tmp/apache-maven.tar.gz ${BASE_URL}/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && echo "${SHA}  /tmp/apache-maven.tar.gz" | sha256sum -c - \
  && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
  && rm -f /tmp/apache-maven.tar.gz \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn

ENV MAVEN_HOME /usr/share/maven
ENV MAVEN_CONFIG "$USER_HOME_DIR/.m2"

COPY mvn-entrypoint.sh /usr/local/bin/mvn-entrypoint.sh
COPY settings-docker.xml /usr/share/maven/ref/
```



/usr/share/maven/ref/repository

### maven+docker+gitlab-runner+jdk(感觉不对废弃,找不到apline安装包)

```dockerfile
FROM maven:alpine

RUN apk add --update --no-cache \
    bash \
    ca-certificates \
    git \
    openssl \
    tzdata \
    wget \
    curl

# docker
ENV VERSION "18.06.0-ce"
RUN curl -L -o /tmp/docker-$VERSION.tgz https://download.docker.com/linux/static/stable/x86_64/docker-$VERSION.tgz \
    && tar -xz -C /tmp -f /tmp/docker-$VERSION.tgz \
    && mv /tmp/docker/docker /usr/bin \
 
# gitlab-runner 
RUN adduser -D -S -h /home/gitlab-runner gitlab-runner

ARG DOCKER_MACHINE_VERSION
ARG DUMB_INIT_VERSION

COPY gitlab-runner-linux-amd64 /usr/bin/gitlab-runner
COPY checksums /tmp/
RUN chmod +x /usr/bin/gitlab-runner && \
    ln -s /usr/bin/gitlab-runner /usr/bin/gitlab-ci-multi-runner && \
    gitlab-runner --version && \
    mkdir -p /etc/gitlab-runner/certs && \
    chmod -R 700 /etc/gitlab-runner && \
    wget -q https://github.com/docker/machine/releases/download/v${DOCKER_MACHINE_VERSION}/docker-machine-Linux-x86_64 -O /usr/bin/docker-machine && \
    chmod +x /usr/bin/docker-machine && \
    docker-machine --version && \
    wget -q https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64 -O /usr/bin/dumb-init && \
    chmod +x /usr/bin/dumb-init && \
    dumb-init --version && \
    sha256sum -c -w /tmp/checksums

COPY entrypoint /
RUN chmod +x /entrypoint

VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]
ENTRYPOINT ["/usr/bin/dumb-init", "/entrypoint"]
CMD ["run", "--user=gitlab-runner", "--working-directory=/home/gitlab-runner"] 
```







### 常见问题总结

1. 注册之后，运行时找不到runner,一直提示pending

   解决：在runner设置里勾选上`Run untagged jobs`

   - [x]  Indicates whether this runner can pick jobs without tags

2. 使用`docker`注册时，镜像用`docker:stable`在配置文件`config.toml`添加` volumes = ["/var/run/docker.sock:/var/run/docker.sock","/cache"]`

   ```toml
   concurrent = 1
   check_interval = 0
   
   [[runners]]
     name = "test"
     url = "http://gitlab/"
     token = "8db125c537f652e20349100517a4d6"
     executor = "docker"
     [runners.docker]
       tls_verify = false
       image = "docker:stable"
       privileged = false
       disable_cache = false
       volumes = ["/var/run/docker.sock:/var/run/docker.sock","/cache"]
       shm_size = 0
     [runners.cache]
   ```

3. 注册后，无权限操作`mkdir: can't create directory '/home/gitlab-runner/builds/': Permission denied `

   解决：通过`gitlab-runner `用户进行注册，[官网注册教程](https://docs.gitlab.com/runner/register/index.html#gnu-linux)

   ```
   docker run --rm -t -i -v /dockerdata/v-gitlab-runner/config:/etc/gitlab-runner --name gitlab_gitlab-runner gitlab/gitlab-runner register
   ```

   



脚本语法：

https://docs.gitlab.com/ee/ci/yaml/README.html



[安装usermode](https://github.com/chrootLogin/docker-nextcloud/issues/3)

```bash
RUN echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories
RUN apk --no-cache add shadow 
```

[使用usermode](http://blog.51cto.com/zhaochj/1309903)

```bash
#修改用户gitlab-runner到root组
usermod -g root gitlab-runner
#查看用户属于的组
id gitlab-runner
#改变文件的组为root,原来的组为docker
chown :root /var/run/docker.sock
```

docker添加组

https://stackoverflow.com/questions/49955097/how-to-add-a-user-group-in-alpine-linux-to-prevent-your-app-to-run-as-root

