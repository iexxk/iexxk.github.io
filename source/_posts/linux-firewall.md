---
title: linux-firewall
date: 2018-11-28 18:26:11
updated: 2020-09-02 16:29:58
categories: Linux
tags: [linux,iptables]
---

## 防火墙配置

### iptables

```
systemctl status iptables.service
```





防火墙端口配置需要放到哪两句之前

[解决Linux:No route to host](https://my.oschina.net/vright/blog/842685)

### firewall

```
# 添加端口7000-7005/17000-17005
firewall-cmd --zone=public --add-port=7000/tcp --permanent
# 重载配置
firewall-cmd --reload
# 检查防火墙规则
firewall-cmd --list-all
# ports: 7000/tcp 7001/tcp 7002/tcp 7003/tcp 7004/tcp 7005/tcp 17005/tcp 17004/tcp 17003/tcp 17002/tcp 17001/tcp 17000/tcp
# 查看防火墙状态
firewall-cmd --state
# 临时关闭防火墙,重启后会重新自动打开
systemctl restart firewalld
#关闭
systemctl stop firewalld.service
开机禁用
systemctl disable firewalld.service
```













