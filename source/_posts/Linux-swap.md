---
title: centos7设置交换分区
date: 2019-03-15 01:17:11
updated: 2019-03-15 11:25:26
categories: Linux
tags: [Linux,swap]
---

## centos设置交换分区之阿里云

交换分区是在内存不足的情况下，存储长期不活跃的内存，但是性能受硬盘影响，下降10倍不等，固态稍微好一点，机械硬盘简直卡死建议不设置

##### 添加交换分区

1. 创建交换分区文件`dd if=/dev/zero of=/home/swap bs=1024 count=3764224`其中**3764244=1024x2x实际内存大小(M)**其中2代表虚拟内存是实际内存的2倍
2. 设置交换分区文件`mkswap /home/swap`
3. 启用交换分区`swapon /home/swap`
4. 设置开机有效`echo "/home/swap swap swap defaults 0 0" >> /etc/fstab`
5. 重启`reboot`非必须，然后执行`df -h`就可以看到swap有值了

##### 删除交换分区

1. 停止swap分区`swapoff /home/swap`
2. 删除swap分区`rm -fr /home/swap`
3. 删除开机启动，在`/etc/fstab`删除行`/home/swap swap swap defaults 0 0`即可