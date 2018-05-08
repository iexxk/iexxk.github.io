---
title: 阿里云服务器增加交换空间
date: 2017-09-17 16:56:37
updated: 2018-04-25 20:47:32categories: Linux
tags: [centos,阿里云,交换空间]
---
```shell
#查看系统空间使用情况
free -h
#查看分区使用
df -h
#生成4G大小文件在/home目录下,取名swapflie
sudo dd if=/dev/zero of=/home/swapflie bs=1M count=4096
#把这个文件转换为swap分区
sudo /sbin/mkswap /home/swapflie
#使分区生效
sudo /sbin/swapon /home/swapflie
```

### 参考：

[Docker Swarm搭建Gitlab](http://www.bijishequ.com/detail/252453?p=)