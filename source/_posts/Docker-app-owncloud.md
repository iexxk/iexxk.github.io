---
title: Docker 应用之owncloud
date: 2018-02-28 17:27:09
updated: 2018-02-28 17:53:29
categories: Docker
tags: [Docker,ossfs,owncloud]
---

## Docker 应用之owncloud

官网：[library/owncloud](https://hub.docker.com/_/owncloud/)

默认会创建挂载卷`-v /<mydatalocation>:/var/www/html`

细分挂载卷

- `-v /<mydatalocation>/apps:/var/www/html/apps` installed / modified apps
- `-v /<mydatalocation>/config:/var/www/html/config` local configuration
- `-v /<mydatalocation>/data:/var/www/html/data` the actual data of your ownCloud （网盘文件）

#### 安装

```bash
docker pull owncloud
#默认安装，会默认创建一个挂载卷
docker run -d -p 14007:80 owncloud:8.1
#将网盘文件存储指向到oss，注意挂载目录的权限问题，否则没权限操作会报错
docker run -v /ossfs/owncloud:/var/www/html/data -d -p 14007:80 owncloud:latest
```

#### 体验

虽然成功存储到了oss里面但是极度卡，就算是阿里云内网ossfs，一样的卡，因此放弃存到ossfs,可以考虑备份放到ossfs