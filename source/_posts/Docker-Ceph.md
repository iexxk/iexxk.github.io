---
title: Docker-Ceph
date: 2018-09-30 15:13:34
updated: 2018-12-12 10:47:58
categories: Docker
tags: [Ceph]
---

# docker 统一存储之ceph

## 知识

#### [ceph核心服务](http://docs.ceph.com/docs/master/start/intro/)

1. MonItor(`mon`)  监视器

   维护集群状态的映射，包括监视器映射，管理器映射，OSD映射和CRUSH映射。这些映射是Ceph守护进程相互协调所需的关键集群状态。监视器还负责管理守护进程和客户端之间的身份验证。冗余和高可用性通常至少需要三个监视器。

2. Managers(`mgr`)  管理器

   守护程序（ceph-mgr）负责跟踪运行时指标和Ceph集群的当前状态，包括存储利用率，当前性能指标和系统负载。 Ceph Manager守护进程还托管基于python的插件来管理和公开Ceph集群信息，包括基于Web的Ceph Manager Dashboard和REST API。高可用性通常至少需要两个管理器。

3. OSDs(`osd_ceph_disk`) 对象存储守护进程

   存储数据，处理数据复制，恢复，重新平衡，并通过检查其他Ceph OSD守护进程来获取心跳，为Ceph监视器和管理器提供一些监视信息。冗余和高可用性通常至少需要3个Ceph OSD。

4. MDSs(`mds`) Ceph元数据服务器

   代表Ceph文件系统存储元数据（即，Ceph块设备和Ceph对象存储不使用MDS）。 Ceph元数据服务器允许POSIX文件系统用户执行基本命令（如ls，find等），而不会给Ceph存储集群带来巨大负担。



#### 问题

1. 断电关机重启问题，如果是安装在容器里，面临自动挂载和卸载问题

   如果挂载了关机时，容器先关闭，导致卸载出问题，一直关不了机

   开机时重新挂载，看不到数据问题

2. 集群部署，osd服务的` privileged: true`特权模式不支持，导致不能操作mount相关

3. 采用`docker plugin install rexray/rbd`插件模式挂载，服务的挂载目录不能更改，且外部需要安装ceph基本组件（考虑是否部分服务安装主机上，可解决123问题）



### 安装

#### 重新部署执行

`docker run -d --privileged=true -v /dev/:/dev/ -e OSD_DEVICE=/dev/sda ceph/daemon zap_device`

并清理目录

1. 三台机执行，其中`MON_IP`替换本机ip

   ```bash
   docker run -d \
           --name=mon \
           --net=host \
           -v /etc/ceph:/etc/ceph \
           -v /var/lib/ceph/:/var/lib/ceph/ \
           -e MON_IP=192.168.1.230 \
           -e CEPH_PUBLIC_NETWORK=192.168.1.0/24 \
           ceph/daemon mon
   ```

   该部不能通过集群stack部署，因为`--net=host`是指用主机网络

2. 然后复制目录`/dockerdata/ceph/data`到另一台机，复制`/dockerdata/ceph/config/bootstrap*`到另一台机

3. 启动第二台，如果有第三台，第三台同理

4. 执行`docker exec mon ceph -s`就可以看到两台了

   ```bash
   [root@environment-test1 ceph]#  docker exec mon ceph -s
     cluster:
       id:     cf6e2bed-0eb6-4ba1-9854-e292c936ea0f
       health: HEALTH_OK
    
     services:
       mon: 2 daemons, quorum lfadmin,environment-test1
       mgr: no daemons active
       osd: 0 osds: 0 up, 0 in
    
     data:
       pools:   0 pools, 0 pgs
       objects: 0  objects, 0 B
       usage:   0 B used, 0 B / 0 B avail
       pgs:     
   ```

5. 添加osd,需要先在主机上添加一块新硬盘,执行`lsblk`查看硬盘编号,硬盘非空，会启动报错，如何清空看[磁盘格始化(删除所有分区)](),单个分区`sda5`不成功，最后只好全磁盘格式化

   ```bash
   docker run -d \
           --net=host \
           --name=ceph_osd \
           --restart=always \
           -v /etc/ceph:/etc/ceph \
           -v /var/lib/ceph/:/var/lib/ceph/ \
           -v /dev/:/dev/ \
           --privileged=true \
           -e OSD_FORCE_ZAP=1 \
           -e OSD_DEVICE=/dev/sda \
           ceph/daemon osd_ceph_disk
   ```

6. 执行`docker exec mon ceph -s`就可以看到两台了和一个**osd**了,但是空间详情看不到，需要运行mds和rgw服务

   ```bash
   [root@environment-test1 ~]# docker exec mon ceph -s
     cluster:
       id:     cf6e2bed-0eb6-4ba1-9854-e292c936ea0f
       health: HEALTH_WARN
               no active mgr
    
     services:
       mon: 2 daemons, quorum lfadmin,environment-test1
       mgr: no daemons active
       osd: 1 osds: 1 up, 1 in
    
     data:
       pools:   0 pools, 0 pgs
       objects: 0  objects, 0 B
       usage:   0 B used, 0 B / 0 B avail
       pgs: 
   ```

7. 添加 mgr

   ```bash
   docker run -d \
           --net=host \
           --name=mgr \
           -v /dockerdata/ceph/data:/etc/ceph \
           -v /dockerdata/ceph/config/:/var/lib/ceph/ \
           ceph/daemon mgr
   ```

8. 添加 mds

   ```
   
   docker run -d \
           --net=host \
           --name=mds \
           -v /dockerdata/ceph/data:/etc/ceph \
           -v /dockerdata/ceph/config/:/var/lib/ceph/ \
           -e CEPHFS_CREATE=1 \
           ceph/daemon mds
   ```

9. 添加 rgw

   ```bash
   docker run -d \
           --name=rgw \
           -p 80:80 \
           -v /dockerdata/ceph/data:/etc/ceph \
           -v /dockerdata/ceph/config/:/var/lib/ceph/ \
           ceph/daemon rgw
   ```

10. 再次执行`docker exec mon ceph -s`查看,就可以看到空间信息了

    ```shell
    [root@environment-test1 ~]# docker exec mon ceph -s
      cluster:
        id:     cf6e2bed-0eb6-4ba1-9854-e292c936ea0f
        health: HEALTH_WARN
                1 MDSs report slow metadata IOs
                Reduced data availability: 24 pgs inactive
                Degraded data redundancy: 24 pgs undersized
                too few PGs per OSD (24 < min 30)
     
      services:
        mon: 2 daemons, quorum lfadmin,environment-test1
        mgr: environment-test1(active)
        mds: cephfs-1/1/1 up  {0=environment-test1=up:creating}
        osd: 1 osds: 1 up, 1 in
     
      data:
        pools:   3 pools, 24 pgs
        objects: 0  objects, 0 B
        usage:   2.0 GiB used, 463 GiB / 465 GiB avail
        pgs:     100.000% pgs not active
                 24 undersized+peered
    ```

### 使用

测试发现只有一个osd挂载失败，因此在两台电脑都添加osd，并都挂载

1. 首先查看登陆用户名和密码

   ```shell
   [root@environment-test1 ~]# cat /dockerdata/ceph/data/ceph.client.admin.keyring 
   [client.admin]
   	key = AQDTqMFbDC4UAxAApyOvC8I+8nA5PMK1bHWDWQ==
   	auid = 0
   	caps mds = "allow"
   	caps mgr = "allow *"
   	caps mon = "allow *"
   	caps osd = "allow *"
   ```

2. 创建挂载目录

   ```shell
   [root@lfadmin mnt]# mkdir /mnt/mycephfs
   ```

3. 挂载

   ```shell
   [root@lfadmin mnt]# mount -t ceph 192.168.1.213,192.168.1.230,192.168.1.212:/ /dockerdata/cephdata -o name=admin,secret=AQCu98JblQgRChAAskEmJ1ekN2Vasa9Chw+gvg==
   ```

4. 设置开机自动挂载?

5. 取消挂载`umount /mnt/mycephfs/` 如果被占用，关闭占用程序和窗口



   docker exec ea8577875af3 ceph osd tree

## 测试

1. 两台节点，一台当掉，不能访问挂载目录





## 集成部署

```yaml
version: "3.6"

networks:
  hostnet:
    external: true
    name: host

services:
  mon212:
    restart: always
    image: ceph/daemon
    command: mon
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    environment:
      MON_IP: 192.168.1.212
      CEPH_PUBLIC_NETWORK: 192.168.1.0/24
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == worker]
  mon213:
    restart: always
    image: ceph/daemon
    command: mon
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    environment:
      MON_IP: 192.168.1.213
      CEPH_PUBLIC_NETWORK: 192.168.1.0/24
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == lfadmin]
  mon230:
    restart: always
    image: ceph/daemon
    command: mon
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    environment:
      MON_IP: 192.168.1.230
      CEPH_PUBLIC_NETWORK: 192.168.1.0/24
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == environment-test1]
  mgr230:
    restart: always
    image: ceph/daemon
    command: mgr
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == environment-test1]
  mds230:
    restart: always
    image: ceph/daemon
    command: mds
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    environment:
      CEPHFS_CREATE: 1
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == environment-test1]   
  rgw230:
    restart: always
    image: ceph/daemon
    command: rgw
    networks:
      hostnet: {}
    volumes:
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph/
    ports:  
      - target: 80
        published: 14002   #只有worker能访问该端口
        protocol: tcp
        mode: host  #版本要求3.2      
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == environment-test1]          
# osd挂载需要特权模式（privileged=true），目前不支持        
#  osd213:
#    restart: always
#    image: ceph/daemon
#    command: osd_ceph_disk
#    privileged: true
#    networks:
#      hostnet: {}
#    volumes:
#      - /dockerdata/ceph/data:/etc/ceph
#      - /dockerdata/ceph/config/:/var/lib/ceph/
#      - /dev/:/dev/
#    environment:
#      OSD_FORCE_ZAP: 1
#      OSD_DEVICE: /dev/sda
#    deploy:
#      replicas: 1
#      restart_policy:
#        condition: on-failure
#      placement:
#        constraints: [node.hostname == lfadmin]
#  osd230:
#    restart: always
#    image: ceph/daemon
#    command: osd_ceph_disk
#    privileged: true
#    networks:
#      hostnet: {}
#    volumes:
#      - /dockerdata/ceph/data:/etc/ceph
#      - /dockerdata/ceph/config/:/var/lib/ceph/
#      - /dev/:/dev/
#    environment:
#      OSD_FORCE_ZAP: 1
#      OSD_DEVICE: /dev/sda
#    deploy:
#      replicas: 1
#      restart_policy:
#        condition: on-failure
#      placement:
#        constraints: [node.hostname == environment-test1]
        
```







### 注意

swarm 不支持`  privileged: true`特权模式，所以使用集群部署时，提示没有权限



### 磁盘格始化(删除所有分区)

查看分区情况`lsblk`

```bash
[root@environment-test1 ~]# lsblk
NAME            MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda               8:0    0 465.8G  0 disk 
├─sda1            8:1    0  70.9G  0 part 
├─sda2            8:2    0     1K  0 part 
├─sda5            8:5    0 105.1G  0 part 
├─sda6            8:6    0   145G  0 part 
└─sda7            8:7    0 144.7G  0 part 
sdb               8:16   0 465.8G  0 disk 
├─sdb1            8:17   0   200M  0 part /boot/efi
├─sdb2            8:18   0     1G  0 part /boot
└─sdb3            8:19   0 464.6G  0 part 
  ├─centos-root 253:0    0   408G  0 lvm  /
  ├─centos-swap 253:1    0   5.8G  0 lvm  [SWAP]
  └─centos-home 253:2    0    50G  0 lvm  /home
```

格式化磁盘`mkfs.ext4 /dev/sda`，如果是格式化一个区，跟上特定数字，例如`mkfs.ext4 /dev/sda5`

```bash
[root@environment-test1 ~]# mkfs.ext4 /dev/sda
mke2fs 1.42.9 (28-Dec-2013)
/dev/sda is entire device, not just one partition!
无论如何也要继续? (y,n) y
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
30531584 inodes, 122096646 blocks
6104832 blocks (5.00%) reserved for the super user
第一个数据块=0
Maximum filesystem blocks=2271215616
3727 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
	102400000

Allocating group tables: 完成                            
正在写入inode表: 完成                            
Creating journal (32768 blocks): 完成
Writing superblocks and filesystem accounting information: 完成 
```

再次查看

```bash
[root@environment-test1 ~]# lsblk
NAME            MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda               8:0    0 465.8G  0 disk 
sdb               8:16   0 465.8G  0 disk 
├─sdb1            8:17   0   200M  0 part /boot/efi
├─sdb2            8:18   0     1G  0 part /boot
└─sdb3            8:19   0 464.6G  0 part 
  ├─centos-root 253:0    0   408G  0 lvm  /
  ├─centos-swap 253:1    0   5.8G  0 lvm  [SWAP]
  └─centos-home 253:2    0    50G  0 lvm  /home
```

### 减少（压缩）分区空间（大小）

[CentOS Linux如何无损调整分区大小（XFS文件系统）](http://www.cuwww.com/help/detail-78.html)  : 没有做到无损

没找到无损调整的方法



https://www.linuxidc.com/Linux/2016-06/132270.htm

http://blog.51cto.com/happyliu/1902022















### 参考

[[喵咪Liunx(7)]Ceph分布式文件共享解决方案](https://my.oschina.net/wenzhenxi/blog/1845710)

https://tobegit3hub1.gitbooks.io/ceph_from_scratch/content/usage/index.html

[swarm脚本部署](https://github.com/sepich/ceph-swarm/blob/master/docker-compose.yml)