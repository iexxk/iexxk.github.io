---
title: docker-volume-use
date: 2018-03-12 10:58:46
updated: 2018-08-07 09:57:55
categories: Docker
tags: [docker,swarm,gluterfs]
---

## docker 挂载卷应用

### 基础知识

> 官网说明[Use bind mounts](https://docs.docker.com/storage/bind-mounts/)
>
> 官网compose文件：[Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)

bind 挂载，就是宿主机路径对应容器路径，该挂载需要先创建目录，简称`/path:/path`

volume挂载，不需要提前创建目录，他是以volume形式，简称`volume-name:/path`

其中`z`和`Z`的使用,eg:`/path:/path:z`

`z`小写的是可以容器共享

`Z`大写的是私有，容器不可共享

`ro`只读挂载

#### 思路

利用gluterfs作为分布式文件系统做同步用，利用虚拟机挂载一个volume专门的存储硬盘

#### 实现

##### 常用命令

```Bash
fdisk -l #查看磁盘
#mount [-参数] [设备名称] [挂载点]
mount /dev/sdb /mnt/test
#umount [设备名称或挂载点]
umount mnt/test
#gluster卷状态[status\start\stop\delete]
gluster volume status v-portainer
#节点添加与删除[probe\detach]
gluster peer detach home
#节点连接状态，没有卷的情况容易端口连接，删除添加节点可解决
gluster peer status
```

##### 单步步骤

```bash
mkdir /dockerdata #创建数据存储盘
#虚拟机挂载该磁盘，作为存储，因为阿里云没有多余磁盘，所有不挂载，直接存到/dockerdata
mount /dev/sdb /dockerdata 
df -h #查看是否挂载成功
#设置开机自动挂在该目录
echo "dev/sdb /dockerdata ext4 defaults 0 0">>/etc/fstab
mkdir /dockerdata/v-portainer
#创建分布式存储卷，force忽略在root目录创建挂在卷的警告
gluster volume create v-portainer replica 2 home:/dockerdata/v-portainer xuanps:/dockerdata/v-portainer force
#启动分布式存储卷
gluster volume start v-portainer
#创建挂载目录
mkdir /volume/v-portainer
#挂载存储卷目录，似乎挂载才会同步
mount -t glusterfs home:/v-portainer /volume/v-portainer
#设置开机挂载,两台单独设置
echo "home:/v-portainer /volume/v-portainer glusterfs defaults 0 1" >> /etc/fstab
#部署应用
docker stack deploy -c docker-compose.yml gitlab
```

##### 问题总结

1. 使用之后，存储数据受网络印象，导致部分应用因为长时间连接不上而导致，不能启动，因此搁置
2. 如果出现节点disconnect，在disconnect节点执行`systemctl restart glusterd`重启