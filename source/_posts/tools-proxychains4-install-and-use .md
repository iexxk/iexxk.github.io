---
title: Linux下安装与使用proxychains4
date: 2017-12-06 11:10:38
updated: 2018-12-12 10:47:58categories: 工具
tags: [Tools,proxychains4]
---
### proxychains4介绍

[proxychains4](https://github.com/rofl0r/proxychains-ng/releases)是一款linux代理设置软件，在需要代理的命令前加proxychains4就可了。

### [Linux安装](https://www.dropbox.com/install-linux)

##### 对应的图文百度经验教程

[centos7 安装使用proxychains4](https://jingyan.baidu.com/article/148a1921f5c5fe4d71c3b105.html)

```shell
yum -y install gcc automake autoconf libtool make #安装make编译工具
git clone https://github.com/rofl0r/proxychains-ng.git #下载，需要先安装git
cd proxychains-ng 
./configure #配置
sudo make && sudo make install #编译安装
sudo cp ./src/proxychains.conf /etc/proxychains.conf #提取配置文件
cd .. && rm -rf proxychains-ng #删除安装文件
sudo vim /etc/proxychains.conf #编辑配置文件（修改最后一行为 socks5 127.0.0.1 1080）这个对应你的代理地址
```

#### 测试

```sh
proxychains4 wget www.google.com #如果没提示错误，然后当前目录会多一个index.html
rm index.html #清除测试垃圾
```

#### 使用

```
proxychains4 <命令>
#eg
proxychains4 bash #该终端的命令自动代理 ，退出exit
proxychains4 firefox #火狐浏览器代理模式
```

