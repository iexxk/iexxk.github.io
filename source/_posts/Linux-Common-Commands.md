---
title: linux常用命令
date: 2016-09-05 15:25:52
updated: 2017-07-03 23:11:36categories: Linux
tags: [linux,命令,后台]
---
# 端口
管理数据库,文件服务等端口，关闭了外部无法访问

>* 开启端口

```bash
firewall-cmd --zone=public --add-port=3306/tcp
```

>* 关闭端口

```bash
firewall-cmd --zone=public --remove-port=3306/tcp
```