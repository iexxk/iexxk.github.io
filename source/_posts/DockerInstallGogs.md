---
title: Docker-install-Gogs
date: 2019-02-14 22:54:43
updated: 2019-02-14 23:04:55
categories: Docker
tags: [Gogs]
---

### gitlab类似仓库Gogs

Gogs内存占用小

部署脚本`docker-compose.yml`

```dockerfile
version: '3'

services:
  gogs:
    restart: always
    image: gogs/gogs
    ports:
      - "14080:3000"
      - "14022:22"
    volumes:   
      - /dockerdata/v-gogs:/data
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == xuanps]
```

第一次运行需要初始化，网页里面设置见[Application](https://github.com/gogs/gogs/tree/master/docker#application)

后面可以通过脚本`/dockerdata/v-gogs/gogs/conf/app.ini`修改所有配置

[github:gogs/gogs](https://github.com/gogs/gogs/tree/master/docker)

[app.ini配置文档](https://gogs.io/docs/advanced/configuration_cheat_sheet.html)

### 镜像仓库设置

