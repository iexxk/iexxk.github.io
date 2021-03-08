---
title: Docker-volume-plugin
date: 2018-03-04 22:30:39
updated: 2018-12-12 10:47:58
categories: Docker
tags: [Docker,volume]
---

## docker 安装docker-volume-glusterfs

前提，首先安装好GlusterFS分布式文件系统，可以参考[centos7 安装 GlusterFS]()

#### [sapk/docker-volume-gluster](https://github.com/sapk/docker-volume-gluster)安装(弃)

不足：无法删除volume，且无法复用

```bash
#安装插件，三台主机都安装（保险起见）
docker plugin install sapk/plugin-gluster
# docker volume create --driver sapk/plugin-gluster --opt voluri="<volumeserver>,<otherserver>,<otheroptionalserver>:<volumename>" --name test
#volumeserver 主机名，可以指定多个，volumenam是 GlusterFS文件系统的挂载劵名，test是swarm挂载卷名
docker volume create --driver sapk/plugin-gluster --opt voluri="worker,home,xuanps:swarm-volume" --name test
#运行ubuntu容器进行测试
docker run -v test:/mnt --rm -ti ubuntu
#进去之后创建文件，其他系统盘也能看到该文件了， 但是其他系统不会创建挂载卷
echo "hello">/mnt/testfile

```

docker-compose 使用

```properties
volumes:
  some_vol:
    driver: sapk/plugin-gluster
    driver_opts:
      voluri: "<volumeserver>:<volumename>"
```



#### [calavera/docker-volume-glusterfs](https://github.com/calavera/docker-volume-glusterfs)官方安装（***废弃***   测试时发现运行找不到插件，太老了，换新插件）

```bash
#---------------------------废弃，网络原因下载不下来--------------------------------
#为了环境干净，安装docker golang容器工具（--rm参数，运行后销毁容器）
docker run -v /tmp/bin:/go/bin \
--rm golang go get github.com/golang/example/hello/...
#测试，执行该命令会输出Hello, Go examples!，如果没输出，说明容器环境和主机环境不一致
/tmp/bin/hello
#----------------准备工作完成正式开始安装---------------------------------------------------------
#通过golang容器工具下载插件，下载到/tmp/bin目录
docker run -v /tmp/bin:/go/bin --rm golang go get github.com/calavera/docker-volume-glusterfs
```

手动去[下载](https://github.com/calavera/docker-volume-glusterfs/releases),通过sftp等工具传到服务器

```bash
mv docker-volume-glusterfs_linux_amd64 docker-volume-glusterfs   #重命名
cp ./docker-volume-glusterfs /usr/bin #放到bin目录
chmod 777 /usr/bin/docker-volume-glusterfs #添加权限
#其他两台主机，然后复制到其他服务器上
scp root@10.14.0.1:~/docker-volume-glusterfs ~
#依次放到bin目录添加权限
cp ~/docker-volume-glusterfs /usr/bin 
chmod 777 /usr/bin/docker-volume-glusterfs
# 三台主机都执行该命令，该命令会前端运行
docker-volume-glusterfs -servers xuanps:worker:home
# 测试使用
sudo docker run --volume-driver glusterfs --volume swarm-volume:/data alpine ash
touch /data/helo
```

### 额外的 docker 卷插件

[官方插件列表](https://docs.docker.com/engine/extend/legacy_plugins/#volume-plugins)

[官方插件商店](https://store.docker.com/search?category=volume&q=&type=plugin)

#### [rancher/convoy](https://github.com/rancher/convoy)

主要功能快照、备份、还原

总结：适用于单节点，单主机，的本地卷管理

#### [calavera/**docker-volume-glusterfs**](https://github.com/calavera/docker-volume-glusterfs)

看[centos7 安装 GlusterFS]()

#### [Pure Storage Docker Volume Plugin](https://store.docker.com/plugins/pure-docker-volume-plugin?tab=description)

#### [Hedvig Docker Volume Plugin](https://store.docker.com/plugins/hedvig-docker-volume-plugin)

依赖于hedvig cluster

#### [REX-Ray](https://rexray.readthedocs.io/en/stable/user-guide/schedulers/docker/plug-ins/)

github: [rexray/rexray](https://github.com/rexray/rexray)

参考：[每天5分钟玩转 OpenStack **Rex-Ray**](https://www.ibm.com/developerworks/community/blogs/132cfa78-44b0-4376-85d0-d3096cd30d3f/entry/Swarm_%E5%A6%82%E4%BD%95%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE_%E6%AF%8F%E5%A4%A95%E5%88%86%E9%92%9F%E7%8E%A9%E8%BD%AC_Docker_%E5%AE%B9%E5%99%A8%E6%8A%80%E6%9C%AF_103?lang=en)

...........居然没找到一个合适的提供者

[rexray/cis-nfs](https://github.com/rexray/csi-nfs)  待测试，NFS似乎不满足需求



### 参考

[Docker与Golang的巧妙结合](https://yq.aliyun.com/articles/225444)

[基于 GlusterFS 实现 Docker 集群的分布式存储](https://www.ibm.com/developerworks/cn/opensource/os-cn-glusterfs-docker-volume/index.html)

