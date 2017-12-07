---
title: WSL使用ssh
date: 2017-11-22 22:12:28
categories: Ubuntu
tags: [ssh,ubuntu,sshd]
---

* ubuntu16.04(bash on window)

如果没有安装wsl(bash on ubuntu)参考[win10 安装ubuntu子系统bash on ubuntu](https://jingyan.baidu.com/article/9faa7231e8fa80473d28cb7b.html)

Ubuntu最新子系统已集成ssh客户端和服务端，只需要简单配置

如果没有安装参考[Ubuntu17.04 开启远程连接ssh服务端](https://jingyan.baidu.com/article/359911f5a5b74857fe0306c4.html)

1. 备份`sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`
2. 修改配置文件`sudo vim /etc/ssh/sshd_config`

```properties
Port 2200 # 端口改为2200，22端口已被占用
ListenAddress 0.0.0.0 # 取消注释
#StrictModes yes # 注释
PasswordAuthentication yes # 允许密码登录
```

3. 启动ssh服务`sudo service ssh start`

4. 检查服务`ps -e |grep ssh` 如果有sshd代表启动成功

5. 测试是否可以连接`ssh -p 2200 xuan@127.0.0.1`用户名一般为wsl子系统@服务前面的名字,密码为系统登陆密码

6. 如果需要远程连接需要开放防火墙端口2200

   参考：[win10 远程访问tomcat，开放8080端口](https://jingyan.baidu.com/article/eae07827456a821fed54856f.html)

