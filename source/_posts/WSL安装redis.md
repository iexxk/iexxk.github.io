---
title: WSL安装gcc
date: 2017-07-18 17:34:28
categories: Ubuntu
tags: [gcc,ubuntu,redis]
---

### 环境

* ubuntu16.04(bash on window)

#### 安装

1. `sudo apt-get update`更新源
2. `sudo apt-get upgrade`更新软件
3. `sudo apt-get install build-essential`安装编译环境（包括gcc）
4. `sudo apt-get install tcl8.5`安装tcl8.5
5. `wget http://download.redis.io/releases/redis-stable.tar.gz`
6. `tar xzf redis-stable.tar.gz`
7. `cd redis-stable`
8. `make`
9. `sudo make install`
10. `cd utils/`
11. `sudo ./install_server.sh`
12. `sudo service redis_6379 start`
13. `sudo service redis_6379 stop`




安装结果：

Port           : 6379
Config file    : /etc/redis/6379.conf
Log file       : /var/log/redis_6379.log
Data dir       : /var/lib/redis/6379
Executable     : /usr/local/bin/redis-server
Cli Executable : /usr/local/bin/redis-cli



参考：

# Windows 10 Linux子系统 （wsl）学习手记