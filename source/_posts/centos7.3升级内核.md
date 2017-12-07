---
title: centos7.3升级内核
date: 2017-09-19 18:13:37
categories: centos
tags: [centos,内核]
---
### centos7.3升级内核

```shell
#查看内核版本
uname -a
uname -r
#导入elrepo的key
rpm -import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
#安装elrepo的yum
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
#查看内核相关包
yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
#安装kernel-ml.x86_64主线稳定版
yum -y --enablerepo=elrepo-kernel install kernel-ml.x86_64 kernel-ml-devel.x86_64
#查看可用内核
cat /boot/grub2/grub.cfg |grep menuentry 
#替换刚刚查看出来的内核名字
grub2-set-default 'CentOS Linux (4.13.2-1.el7.elrepo.x86_64) 7 (Core)'
#查看内核启动项
grub2-editenv list 
#重启
reboot
#查看版本
uname -r
#查看内核
rpm -qa | grep kernel
#删除内核
yum remove kernel-3.10.0-514.26.2.el7.x86_64
```

##### 参考

 [Centos 7/6 内核版本由3.10.0 升级至 4.12.4方法](http://www.jiagoumi.com/work/1167.html)