---
title: Linux-mount
date: 2018-10-17 11:17:09
updated: 2018-10-17 11:40:43
categories: Linux
tags: [Linux,mount]
---

## linux挂载相关命令

**<u>注意挂载操作不要在挂载目录里面操作</u>**

```shell
#查看磁盘分区情况
lsblk
#查看磁盘详情
fdisk -l
#挂载 ，提前建好挂在目录，这句诗挂载sdc设备的第五个分区
mount /dev/sdc5  /mnt/udisk
# 挂载ntfs的系统需要先安装ntfs-3g
yum install ntfs-3g

# 卸载
umount
```

### hyper-v  centos挂载其他vhd 硬盘

`mount: unknown filesystem type 'LVM2_member'`

```bash
fdisk -l
mount /dev/mapper/centos-root /mnt/disk
umount /mnt/disk
```





https://www.howtoforge.com/tutorial/mount-ntfs-centos/