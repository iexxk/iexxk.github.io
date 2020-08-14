---
title: Linux-mount
date: 2018-10-17 11:17:09
updated: 2019-01-24 16:30:21
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

### [腾讯云初始化和挂载硬盘](https://cloud.tencent.com/document/product/362/6735)

1. `fdisk -l`查看磁盘, 如果没有输出硬盘检查云盘状态是否已挂载

   ```verilog
   Disk /dev/vdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
   ```

2. `fdisk /dev/vdb`创建新分区依次输入“n”(新建分区)、“p”(新建主分区)、“1”(使用第1个主分区)，两次回车(使用默认配置)，输入“wq”(保存分区表)

   ```verilog
   Welcome to fdisk (util-linux 2.23.2).
   
   Changes will remain in memory only, until you decide to write them.
   Be careful before using the write command.
   
   Device does not contain a recognized partition table
   Building a new DOS disklabel with disk identifier 0x45f0094c.
   
   Command (m for help): n
   Partition type:
      p   primary (0 primary, 0 extended, 4 free)
      e   extended
   Select (default p): p
   Partition number (1-4, default 1): 1
   First sector (2048-209715199, default 2048): 
   Using default value 2048
   Last sector, +sectors or +size{K,M,G} (2048-209715199, default 209715199): 
   Using default value 209715199
   Partition 1 of type Linux and of size 100 GiB is set
   
   Command (m for help): wq
   The partition table has been altered!
   
   Calling ioctl() to re-read partition table.
   Syncing disks.
   ```

3. `fdisk -l` 检查

   ```
   Disk /dev/vda: 53.7 GB, 53687091200 bytes, 104857600 sectors
   Units = sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk label type: dos
   Disk identifier: 0x000c5e30
   
      Device Boot      Start         End      Blocks   Id  System
   /dev/vda1   *        2048   104857599    52427776   83  Linux
   
   Disk /dev/vdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
   Units = sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk label type: dos
   Disk identifier: 0x45f0094c
   
      Device Boot      Start         End      Blocks   Id  System
   /dev/vdb1            2048   209715199   104856576   83  Linux
   ```

4. `mkdir /data`如果没有创建挂载目录

5. `mkfs.ext3 /dev/vdb1` 格式化硬盘

6. `mount /dev/vdb1 /data`设置挂载

7. `vim /etc/fstab`设置开机启动自动挂载，fstab追加行

   ```
   /dev/vdb1            /data                ext3       defaults              0 0
   ```

   



https://www.howtoforge.com/tutorial/mount-ntfs-centos/