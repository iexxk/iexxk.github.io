---
title: dcoker swarm安装gitlab
date: 2017-12-11 14:54:37
categories: docker
tags: [docker swarm,gitlab]
---



### 环境准备

```sh
sudo docker rm $(docker ps -a -q) #移除所有已停止的镜像
sudo docker swarm leave
sudo docker swarm init --advertise-addr 10.14.0.1
sudo docker swarm join --token SWMTKN-1-1ue26optqse6n6gcaitf6ns7qyiyqo7o6eb6genabxkof6rhid-d6f802lv5logrupqeop0087fx 10.14.0.1:2377
```

### 安装[sameersbn](https://hub.docker.com/u/sameersbn/)/[gitlab](https://hub.docker.com/r/sameersbn/gitlab/)

```sh
#工作节点拉取镜像
sudo docker pull sameersbn/gitlab:10.2.2
sudo docker pull sameersbn/redis:latest
sudo docker pull sameersbn/postgresql:9.6-2
#创建目录,创建到了Dropbox目录
mkdir -p docker/gitlab/postgresql docker/gitlab/redis docker/gitlab/gitlab
```

下载`wget https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml`并修改

为如下内容，主要替换版本`version: '3'`和添加`deploy`以及配置参数

```properties
version: '3'

services:
  redis:
    restart: always
    image: sameersbn/redis:latest
    command:
    - --loglevel warning
    volumes:
    - ~/Dropbox/docker/gitlab/redis:/var/lib/redis:Z
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.role == worker]

  postgresql:
    restart: always
    image: sameersbn/postgresql:9.6-2
    volumes:
    - ~/Dropbox/docker/gitlab/postgresql:/var/lib/postgresql:Z
    environment:
    - DB_USER=gitlab
    - DB_PASS=mimais163
    - DB_NAME=gitlabhq_production
    - DB_EXTENSION=pg_trgm
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.role == worker]

  gitlab:
    restart: always
    image: sameersbn/gitlab:10.2.2
    depends_on:
    - redis
    - postgresql
    ports:
    - "14008:80"
    - "14002:22"
    volumes:
    - ~/Dropbox/docker/gitlab/gitlab:/home/git/data:Z
    environment:
    - DEBUG=false

    - DB_ADAPTER=postgresql
    - DB_HOST=postgresql
    - DB_PORT=5432
    - DB_USER=gitlab
    - DB_PASS=mimais163
    - DB_NAME=gitlabhq_production

    - REDIS_HOST=redis
    - REDIS_PORT=6379

    - TZ=Asia/Kolkata
    - GITLAB_TIMEZONE=Kolkata

    - GITLAB_HTTPS=false
    - SSL_SELF_SIGNED=false

    - GITLAB_HOST=iexxk.com
    - GITLAB_PORT=14008
    - GITLAB_SSH_PORT=14002
    - GITLAB_RELATIVE_URL_ROOT=
    - GITLAB_SECRETS_DB_KEY_BASE=CvpwfRsb5sNpmGRcX5fQFzTNtdkd5pNMK623PVP9rkwLsTDW4VlXMLmT4bKRLVzC
    - GITLAB_SECRETS_SECRET_KEY_BASE=cFdsD8xSKVCShL76hpWP3NdjTCm3XbtV7d3BXB9XZNHclq8n743s3vFTkMg3DppJ
    - GITLAB_SECRETS_OTP_KEY_BASE=P8rH42vPgg5pZ34Nt8t3pwnCBcPXNkjqV8kTxBlQCkFkSCXGhXvDRSGm2bBx593q

    - GITLAB_ROOT_PASSWORD=mimais163
    - GITLAB_ROOT_EMAIL=xuan.fong1@163.com

    - GITLAB_NOTIFY_ON_BROKEN_BUILDS=true
    - GITLAB_NOTIFY_PUSHER=false

    - GITLAB_EMAIL=notifications@example.com
    - GITLAB_EMAIL_REPLY_TO=noreply@example.com
    - GITLAB_INCOMING_EMAIL_ADDRESS=reply@example.com

    - GITLAB_BACKUP_SCHEDULE=daily
    - GITLAB_BACKUP_TIME=01:00

    - SMTP_ENABLED=false
    - SMTP_DOMAIN=www.example.com
    - SMTP_HOST=smtp.qq.com
    - SMTP_PORT=465
    - SMTP_USER=
    - SMTP_PASS=password
    - SMTP_STARTTLS=true
    - SMTP_AUTHENTICATION=login

    - IMAP_ENABLED=false
    - IMAP_HOST=imap.gmail.com
    - IMAP_PORT=993
    - IMAP_USER=mailer@example.com
    - IMAP_PASS=password
    - IMAP_SSL=true
    - IMAP_STARTTLS=false

    - OAUTH_ENABLED=false
    - OAUTH_AUTO_SIGN_IN_WITH_PROVIDER=
    - OAUTH_ALLOW_SSO=
    - OAUTH_BLOCK_AUTO_CREATED_USERS=true
    - OAUTH_AUTO_LINK_LDAP_USER=false
    - OAUTH_AUTO_LINK_SAML_USER=false
    - OAUTH_EXTERNAL_PROVIDERS=

    - OAUTH_CAS3_LABEL=cas3
    - OAUTH_CAS3_SERVER=
    - OAUTH_CAS3_DISABLE_SSL_VERIFICATION=false
    - OAUTH_CAS3_LOGIN_URL=/cas/login
    - OAUTH_CAS3_VALIDATE_URL=/cas/p3/serviceValidate
    - OAUTH_CAS3_LOGOUT_URL=/cas/logout

    - OAUTH_GOOGLE_API_KEY=
    - OAUTH_GOOGLE_APP_SECRET=
    - OAUTH_GOOGLE_RESTRICT_DOMAIN=

    - OAUTH_FACEBOOK_API_KEY=
    - OAUTH_FACEBOOK_APP_SECRET=

    - OAUTH_TWITTER_API_KEY=
    - OAUTH_TWITTER_APP_SECRET=

    - OAUTH_GITHUB_API_KEY=
    - OAUTH_GITHUB_APP_SECRET=
    - OAUTH_GITHUB_URL=
    - OAUTH_GITHUB_VERIFY_SSL=

    - OAUTH_GITLAB_API_KEY=
    - OAUTH_GITLAB_APP_SECRET=

    - OAUTH_BITBUCKET_API_KEY=
    - OAUTH_BITBUCKET_APP_SECRET=

    - OAUTH_SAML_ASSERTION_CONSUMER_SERVICE_URL=
    - OAUTH_SAML_IDP_CERT_FINGERPRINT=
    - OAUTH_SAML_IDP_SSO_TARGET_URL=
    - OAUTH_SAML_ISSUER=
    - OAUTH_SAML_LABEL="Our SAML Provider"
    - OAUTH_SAML_NAME_IDENTIFIER_FORMAT=urn:oasis:names:tc:SAML:2.0:nameid-format:transient
    - OAUTH_SAML_GROUPS_ATTRIBUTE=
    - OAUTH_SAML_EXTERNAL_GROUPS=
    - OAUTH_SAML_ATTRIBUTE_STATEMENTS_EMAIL=
    - OAUTH_SAML_ATTRIBUTE_STATEMENTS_NAME=
    - OAUTH_SAML_ATTRIBUTE_STATEMENTS_FIRST_NAME=
    - OAUTH_SAML_ATTRIBUTE_STATEMENTS_LAST_NAME=

    - OAUTH_CROWD_SERVER_URL=
    - OAUTH_CROWD_APP_NAME=
    - OAUTH_CROWD_APP_PASSWORD=

    - OAUTH_AUTH0_CLIENT_ID=
    - OAUTH_AUTH0_CLIENT_SECRET=
    - OAUTH_AUTH0_DOMAIN=

    - OAUTH_AZURE_API_KEY=
    - OAUTH_AZURE_API_SECRET=
    - OAUTH_AZURE_TENANT_ID=
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.role == worker]
```

启动运行

```sh
docker stack deploy -c docker-compose.yml gitlab
#查看gitlab
docker stack ps gitlab
#停止删除gitlab
docker stack rm gitlab
#创建符合链接，解决ubuntu非root用户导致Dropbox路径不一样，待测试
ln -s /home/xuan/Dropbox /root/Dropbox
```

