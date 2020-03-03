---
title: Linux-System-Clone
date: 2020-02-20 15:20:55
updated: 2020-02-21 14:58:21
categories: Linux
tags: [System,Clone]
---

## 工具介绍

### Mondo Rescue

[官网](http://www.mondorescue.org/)

#### 安装

```bash
wget http://www.mondorescue.org/ftp/centos/7/x86_64/mondorescue.repo
mv mondorescue.repo /etc/yum.repos.d/
yum install mondo
mondoarchive
```



### Relax and Recover

[官网](https://relax-and-recover.org/)，[github](https://github.com/rear/rear)

#### 安装

```bash
yum install syslinux syslinux-extlinux
yum install rear
rear --v
```

资料较少，暂时放弃

##### 参考

[How to Install ReaR (Relax and Recover) on CentOS 7](https://linoxide.com/tools/install-relax-recover-centos-7/)

### Clonezilla 再生龍

[官网](http://clonezilla.nchc.org.tw/clonezilla-live/download/)

