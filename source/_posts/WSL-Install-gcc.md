---
title: WSL安装gcc
date: 2017-07-18 17:34:28
updated: 2017-12-13 10:37:19categories: WSL
tags: [gcc,ubuntu,redis,WSL]
---

* ubuntu16.04(bash on window)
* gcc

```
sudo apt-get update && \
sudo apt-get install build-essential software-properties-common -y && \
sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
sudo apt-get update && \
sudo apt-get install gcc-snapshot -y && \
sudo apt-get update && \
sudo apt-get install gcc-6 g++-6 -y && \
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 && \
sudo apt-get install gcc-4.8 g++-4.8 -y && \
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8;
```

选择默认gcc版本

`sudo update-alternatives --config gcc`

####  安装redis

安装好了要清理下redis的目录

`make distclean`在`make`

在redis目录下

运行服务端

`src/redis-server`

运行客户端

`src/redis-cli`

#### 参考

[[application2000](https://gist.github.com/application2000)/**how-to-install-latest-gcc-on-ubuntu-lts.txt**](https://gist.github.com/application2000/73fd6f4bf1be6600a2cf9f56315a2d91)



## 方法二

`sudo apt-get install build-essential`安装编译环境（包括gcc）