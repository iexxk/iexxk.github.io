---
title: Linux下安装与使用DropBox
date: 2017-12-07 14:26:38
updated: 2017-12-12 18:29:34categories: 工具
tags: [Tools,Dropbox]
---
### DropBox介绍

[DropBox](https://www.dropbox.com/)是一款同步软件，中文名多宝盒，类似网盘，由于平台兼容性比较好，这里用来做ubuntu和windos笔记存储等，还用到了docker数据卷同步（性能待测试）

### [Linux安装](https://www.dropbox.com/install-linux)

##### 对应的图文百度经验教程

[centos7多宝盒切换账号和安装管理脚本](https://jingyan.baidu.com/article/154b4631044be528ca8f410a.html)

[centos7命令行安装多宝箱](https://jingyan.baidu.com/article/90895e0f27e12b64ec6b0b09.html)

```shell
cd ~ #下载安装目录
wget https://clientupdates.dropboxstatic.com/dbx-releng/client/dropbox-lnx.x86_64-39.4.49.tar.gz #下载
tar xzf dropbox-lnx.x86_64-39.4.49.tar.gz #解压
ls #解压后用ls，查看不到改文件，因为是.开头的
cd ~/. <按TAB键> #可以看到
proxychains4 ~/.dropbox-dist/dropboxd #安装,需要使用代理，proxychains4安装见前面的文章
```

##### 授权：

启动后有很多日志，然后复制输出的网址去浏览器访问，不需要本机，任何电脑浏览器都可以

##### 注销：

如果注销账号可以去网页版，取消授权，然后再次执行安装命令可以重新授权

#### 管理工具下载安装与使用

```shell
#下载dropbox.py
proxychains4 wget -O dropbox.py https://www.dropbox.com/download?dl=packages/dropbox.py
chmod +x dropbox.py
#停止dropbox
./dropbox.py stop
killall dropbox
#安装demon(可忽略这一步，这一步是设置系统服务失败遗留)
proxychains4 ./dropbox.py start -i
#安装完成后会自动启动，如果ctrl+c停止不了可以在开一个终端执行./dropbox.py stop
#移动管理工具到安装目录
mv dropbox.py /root/.dropbox/dropbox.py
#添加全局命令，使用链接模式
ln -sf /root/.dropbox/dropbox.py /usr/bin/dropbox
#设置代理
dropbox proxy manual socks5 127.0.0.1 1080
dropbox start #启动
dropbox status #查看状态
dropbox stop #停止
```

#### 额外，这里把dropbox设置成systemctl并未成功，所以未添加开机启动，开机需要手动执行`dropbox start`