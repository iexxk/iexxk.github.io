---
title: Docker 应用之gitlab
date: 2018-01-17 23:40:37
updated: 2019-04-18 17:20:06
categories: Docker
tags: [Docker,gitlab,runner,swarm,statck]
---
## 单机应用gitlab

##### [MySQL](https://store.docker.com/images/mysql)

```shell
#下载
docker pull mysql
#启动mysql容器,返回容器id (-p 3306:3306 指定外部连接端口，不指定外部连接不上)
docker run --name gitlab-mysql -e MYSQL_ROOT_PASSWORD=Mimais163. -d mysql
#连接进入mysql命令行
docker run -it --link gitlab-mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
#MySQL命令
show databases; #显示数据库
quit #退出命令行
```

##### [redis](https://store.docker.com/images/redis)

```shell
#下载
docker pull redis
#启动redis容器
docker run --name gitlab-redis -d redis
```

##### [sameersbn](https://hub.docker.com/u/sameersbn/)/[gitlab](https://hub.docker.com/r/sameersbn/gitlab/)

###### 注 [在 Docker 中使用 GitLab](http://beyondvincent.com/2016/09/19/2016-09-17-use-gitlab-with-docker/)

[sameersbn](https://hub.docker.com/u/sameersbn/)/[gitlab](https://hub.docker.com/r/sameersbn/gitlab/)和[gitlab](https://hub.docker.com/u/gitlab/)/[gitlab-ce](https://hub.docker.com/r/gitlab/gitlab-ce/)区别在于前者需要MySQL和redis,后者集成所有环境

###### [安装法一](https://docs.gitlab.com/omnibus/docker/)

```shell
#下载docker-compose.yml脚本
wget https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml
#安装pwgen密码生产器
yum install pwgen
#生成三个密码
pwgen -Bsv1 64
#修改docker-compose.yml下这三个参数
-GITLAB_SECRETS_DB_KEY_BASE=CvpwfRsb5sNpmGRcX5fQFzTNtdkd5pNMK623PVP9rkwLsTDW4VlXMLmT4bKRLVzC
-GITLAB_SECRETS_SECRET_KEY_BASE=cFdsD8xSKVCShL76hpWP3NdjTCm3XbtV7d3BXB9XZNHclq8n743s3vFTkMg3DppJ
-GITLAB_SECRETS_OTP_KEY_BASE=P8rH42vPgg5pZ34Nt8t3pwnCBcPXNkjqV8kTxBlQCkFkSCXGhXvDRSGm2bBx593q
#运行脚本
docker-compose up
#运行网页www.exxk.me:10080
#用户名root
```

###### 安装法二

```shell
#下载安装
docker pull sameersbn/gitlab
#查看镜像
docker images
#运行  
sudo docker run --detach \
    --hostname gitlab.xuan.com \
    --publish 10443:443 --publish 10080:80 --publish 10022:22 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest
#查看运行的镜像
docker ps
```

访问地址[http://112.74.51.136:10080](http://112.74.51.136:10080)

- 注意开放端口

##### 运行

编辑运行参数文件`vim docker-compose.yml`

```properties
web:
  image: 'gitlab/gitlab-ce:latest'
  restart: always
  hostname: 'gitlab.example.com'
  environment:
    GITLAB_OMNIBUS_CONFIG: |
      external_url 'http://gitlab.example.com:9090'
      gitlab_rails['gitlab_shell_ssh_port'] = 2224
  ports:
    - '9090:9090'
    - '2224:22'
  volumes:
    - '/srv/gitlab/config:/etc/gitlab'
    - '/srv/gitlab/logs:/var/log/gitlab'
    - '/srv/gitlab/data:/var/opt/gitlab'
```

执行`docker-compose up -d` 运行

### [sameersbn/gitlab-ci-multi-runner](https://docs.gitlab.com/runner/install/docker.html)

```shell
#下载
docker pull gitlab/gitlab-runner
#运行
docker run -d --name gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
#注册
docker exec -it gitlab-runner gitlab-runner register
```

执行后进入设置：相关参数见 [ gitlab->project-settings->Pipelines](http://exxk.me:10080/root/test_run/settings/ci_cd)

```shell
#进入设置
Running in system-mode.                            
                                                   
Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
#Specify the following URL during the Runner setup:http://exxk.me:10080/
> http://exxk.me:10080/
Please enter the gitlab-ci token for this runner:
#Use the following registration token during setup:qg78V4rsaxabgULs-cps
> qg78V4rsaxabgULs-cps
Please enter the gitlab-ci description for this runner:
> [dd8f66b4b9ac]: aa
Please enter the gitlab-ci tags for this runner (comma separated):
> cc
Whether to run untagged builds [true/false]:
> [false]: 
Whether to lock Runner to current project [true/false]:
> [false]: 
Registering runner... succeeded                     runner=qg78V4rs
Please enter the executor: docker, parallels, shell, docker+machine, kubernetes, docker-ssh, ssh, virtualbox, docker-ssh+machine:
# 选择runner 运行的环境 这里是docker
> docker
Please enter the default Docker image (e.g. ruby:2.1):
> tomcat
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
```

## 集群应用gitlab

准备工作

```bash
mkdir -p /srv/docker/gitlab/postgresql
mkdir -p /srv/docker/gitlab/redis
mkdir -p /srv/docker/gitlab/gitlab
```

`vim gitlab.yml`见末尾

```bash
#启动gitlab
docker stack deploy -c gitlab.yml gitlab
#查看gitlab
docker stack ps gitlab
#停止删除gitlab
docker stack rm gitlab
#查看服务
docker service ls
#查看服务详情
docker service ps --no-trunc <service id>
```

`gitlab.yml`文件内容

```properties
# gitlab.yml文件
version: '3'
services:
  postgresql:
    image: sameersbn/postgresql:9.6-2
    environment:
      - TZ=Asia/Shanghai
      - DB_NAME=gitlabhq_production
      - DB_USER=gitlab
      - DB_PASS=xxxxx
      - DB_EXTENSION=pg_trgm
    volumes:
      - /srv/docker/gitlab/postgresql:/var/lib/postgresql
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.role == worker]
  redis:
    image: sameersbn/redis:latest
    command:
      - --loglevel warning
    environment:
      - TZ=Asia/Shanghai
    volumes:
    - /srv/docker/gitlab/redis:/var/lib/redis
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
     placement:
        constraints: [node.role == worker]
  gitlab:
    image: sameersbn/gitlab:9.5.4
    environment:
      - TZ=Asia/Shanghai
      - GITLAB_HOST=exxk.me
      - GITLAB_PORT=10080
      - GITLAB_SSH_PORT=10022
      - DB_HOST=postgresql
      - DB_USER=gitlab
      - DB_PASS=xxxx
      - GITLAB_SECRETS_DB_KEY_BASE=xxxxzTNtdkd5pNMK623PVP9rkwLsTDW4VlXMLmT4bKRLVzC
      - GITLAB_SECRETS_SECRET_KEY_BASE=xxxxxjTCm3XbtV7d3BXB9XZNHclq8n743s3vFTkMg3DppJ
      - GITLAB_SECRETS_OTP_KEY_BASE=xxxxxxBcPXNkjqV8kTxBlQCkFkSCXGhXvDRSGm2bBx593q
      - GITLAB_TIMEZONE=Beijing
      - GITLAB_ROOT_PASSWORD=mimais163
      - REDIS_HOST=redis
      - REDIS_PORT=6379
   - SMTP_USER=986905087@qq.com
      - SMTP_PASS=xxxxx
      - SMTP_HOST=smtp.qq.com
      - SMTP_PORT=465
      - SMTP_TLS=true

    volumes:
      - /srv/docker/gitlab/gitlab:/home/git/data
    ports:
      - 10080:80
      - 10022:22
    depends_on:
      - postgresql
      - redis
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
 	placement:
        constraints: [node.role == worker]
```

###### 参考：[compose-v3](https://help.aliyun.com/document_detail/56446.html?spm=a3c0i.o56446zh.a3.3.36e8e022ppja9J#Compose)

额外nginx

```bash
docker service create -p 8080:80 --name webserver nginx
docker service inspect --format="{{json .Endpoint.Spec.Ports}}" webserver
[{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080,"PublishMode":"ingress"}]
docker service update --replicas 1 webserver
```

