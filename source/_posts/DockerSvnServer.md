---
title: Docker-Svn-Server
date: 2018-07-27 16:38:44
updated: 2018-12-12 10:47:58
categories: Docker
tags: [Svn,Docker]
---

### docker运行安装svn服务器

#### [elleflorio/svn-server](https://hub.docker.com/r/elleflorio/svn-server/)

```yaml
version: '3'

services:
  svn:
    restart: always
    image: elleflorio/svn-server
    volumes:
    - /dockerdata/v-svn:/home/svn
    ports:
    - "14009:3690"
    - "14008:80"
```

1. 创建仓库，进入容器执行`svnadmin create --pre-1.6-compatible /home/svn/rep`不考虑兼容,可以不加`--pre-1.6-compatible`

2. 添加用户名和密码`htpasswd -bc /etc/subversion/passwd lx 123456` 其中`lx`是用户名，`123456`是密码，其中`httpasswd`命令参数

   ```sh
   -c：创建一个加密文件；
   -n：不更新加密文件，只将加密后的用户名密码显示在屏幕上；
   -m：默认采用MD5算法对密码进行加密；
   -d：采用CRYPT算法对密码进行加密；
   -p：不对密码进行进行加密，即明文密码；
   -s：采用SHA算法对密码进行加密；
   -b：在命令行中一并输入用户名和密码而不是根据提示输入密码；
   -D：删除指定的用户。
   ```

3. 然后访问`192.168.1.230:14008/svn`就会弹出输入用户名和密码窗口

4. 使用svn客户端输入http://192.168.1.230:14008/svn/rep/就可以检出了

### 注意

1. 由于配置文件放在容器的，因此容器重启会重新设置密码

   解决：

   1. 挂载密码的文件目录
   2. 重新编译[dockerfile](https://github.com/elleFlorio/svn-docker)

参考：[5-使用docker-svn镜像](https://www.jianshu.com/p/0146b5ba69a6)