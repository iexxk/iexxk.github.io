---
title: Docker-Gitlab-official
date: 2018-07-27 13:43:28
updated: 2018-07-27 13:55:46
categories: Docker
tags: [Docker,Gitlab]
---

### 官方版gitlab安装使用

[官网教程](https://docs.gitlab.com/omnibus/docker/)

`docker-statck.yml`文件

```yaml
version: "3.6"
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    ports:
      - "14020:22"
      - "14018:80"
#https      - "14019:443"
    volumes:
      - /dockerdata/v-gitlab-ce/data:/var/opt/gitlab
      - /dockerdata/v-gitlab-ce/logs:/var/log/gitlab
      - /dockerdata/v-gitlab-ce/config:/etc/gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: "from_file('/omnibus_config.rb')"
    configs:
      - source: gitlab_rb
        target: /omnibus_config.rb
    secrets:
      - gitlab_root_password
  gitlab-runner:
    image: gitlab/gitlab-runner:alpine
    deploy:
      mode: replicated
      replicas: 1
configs:
  gitlab_rb:
    external: true
secrets:
  gitlab_root_password:
    external: true
```

portainer->config->name: `gitlab_rb`

```yaml
external_url 'http://192.168.1.230:14018/'
#这里必须设置监听为80，因为是监听容器内的端口
nginx['listen_port'] = 80
#这里要设置ssh端口，不然ssh不能使用
gitlab_rails['gitlab_shell_ssh_port'] = 14020
gitlab_rails['initial_root_password'] = File.read('/run/secrets/gitlab_root_password')
```

portainer->secrets->name: `gitlab_root_password`

```yaml
MySuperSecretAndSecurePass0rd!
```

登陆时用户名为`root`，密码为`gitlab_root_password`的内容



### 额外

1. 进入容器可以执行命令`gitlab-rake gitlab:env:info`更多命令见rake
2. 备份文件`repositories`中`xxx.bundle`可以用git命令解压`git clone xxx.bundle xxx`,详情见`git bundle`打包

