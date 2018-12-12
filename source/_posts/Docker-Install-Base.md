---
title: Docker 安装与使用基础
date: 2017-10-10 10:25:37
updated: 2018-12-12 10:47:58
categories: Docker
tags: [docker,docker-compose]
---
#### 常用命令

```bash
docker ps [-a] #查看运行容器状态，-a 查看所有容器
docker stop <容器id> #停止运行容器
docker rm <容器id> [-f] #删除容器，-f 删除运行的
docker rmi <镜像id> #删除镜像
docker exec -it <容器id> </bin/bash或者sh> 进入容器（bash或者sh）
exit #退出容器
#添加标签
docker node update --label-add <KEY>=<VALUE> <NODE ID|NAME>
#查看节点详细信息
docker node inspect <NODE ID|NAME>
#查看网络
ifconfig
#推镜像到仓库
docker push exxk/gitlab_cloud:tagname
#拉取镜像
docker pull exxk/gitlab_cloud:tagname
#远程连接
sudo docker -H tcp://ip:port <docker名令>
#eg查看远程的又什么镜像
sudo docker -H tcp://10.14.0.4:2375 images
```

### [docker](https://docs.docker.com/engine/installation/linux/docker-ce/centos/#install-using-the-repository)安装

```sh
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum makecache fast
sudo yum install docker-ce
systemctl start docker.service

sudo docker run hello-world
sudo docker version
yum list docker-ce --showduplicates | sort -r
```

#### daemon设置

修改/etc/docker/daemon.json文件

```bash
vim /etc/docker/daemon.json
#改完后重新加载配置
sudo systemctl daemon-reload
#重启docker
sudo systemctl restart docker
```

##### [docker加速阿里云加速地址](https://cr.console.aliyun.com/?spm=5176.2020520152.210.d103.5dbcab35Yw8obw#/accelerator)

```
#等效于添加daemon.json文件
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://*****.mirror.aliyuncs.com"],
  "hosts":["unix:///var/run/docker.sock"]
}
EOF
```

##### [远程访问docker](https://jingyan.baidu.com/article/c843ea0bcf8a2777931e4ae7.html)

###### 方法1

在daemo.json添加`"hosts":["tcp://0.0.0.0:2375","unix:///var/run/docker.sock"]`

hosts 分tcp,uninx,fd三种模式，第一中时tcp指定网络连接方式，0.0.0.0:2375是指所有网络都可以连接，不安全，因此一般会加上stl证书形式，这里我用的局域网，所有没有加证书，指定局域网设置主机所属ip例如网卡2的ip为10.14.0.2，因此设置为10.14.0.2,只有10.14.0这个局域网可以访问，第二种uninx时指本地可以自由连接docker，第三种，理解不是很清楚，不发表见解

###### 方法2（方法1能采用尽量用1）

直接修改服务的启动文件，添加-H参数指定

```sh
#解决portainner添加节点失败centos7.2 修改 /lib/systemd/system/docker.service
#ExecStart=/usr/bin/dockerd
#修改为
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
systemctl daemon-reload
systemctl restart docker.service
```

###### 参考：[docker 远程连接](https://www.jianshu.com/p/7ba1a93e6de4)

### [docker-compose](https://docs.docker.com/compose/install/#uninstallation)安装

##### 法一(当前采用)

```bash
#pip安装方式
pip install docker-compose
#pip卸载方式
pip uninstall docker-compose
```

##### 法二

安装[docker-compose](https://github.com/docker/compose/releases)（以容器类型安装）

##### 法三

```bash
sudo -i
#安装脚本，替换为最新的版本 ，这一步会失败，执行sudo -i
curl -L https://github.com/docker/compose/releases/download/1.15.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
#添加执行权限
chmod +x /usr/local/bin/docker-compose
#测试(失败，需要执行./docker-compose --version  没全局)
docker-compose --version
```

#### 基本常用命令

```bash
docker-compose up -d
docker-compose down
docker-compose stop
docker-compose rm
docker-compose logs
```

### [docker-machine](https://docs.docker.com/machine/install-machine/#installing-machine-directly)

linux

```shell
curl -L https://github.com/docker/machine/releases/download/v0.12.2/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
```

windos git bash

```shell
if [[ ! -d "$HOME/bin" ]]; then mkdir -p "$HOME/bin"; fi && \
curl -L https://github.com/docker/machine/releases/download/v0.12.2/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe" && \
chmod +x "$HOME/bin/docker-machine.exe"
```



### 问题以及解决方法

1. docker inf 出现如下警告

   ```
   WARNING: bridge-nf-call-iptables is disabled
   WARNING: bridge-nf-call-ip6tables is disabled
   ```

   解决：

   `echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables`

   ` echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables`

2. 问题：构建镜像不能用`-`减号命名镜像的名字，使用docker-statck 部署找不到镜像

3. 问题: 执行`sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo`

   ```bash
   [root@lfadmin ~]# sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   已加载插件：fastestmirror, langpacks
   adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
   grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
   Could not fetch/save url https://download.docker.com/linux/centos/docker-ce.repo to file /etc/yum.repos.d/docker-ce.repo: [Errno 12] Timeout on https://download.docker.com/linux/centos/docker-ce.repo: (28, 'Resolving timed out after 30541 milliseconds')
   ```

   解决：

   `vim /etc/yum.repos.d/docker-ce.repo`

   ```properties
   [docker-ce-stable]
   name=Docker CE Stable - $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/$basearch/stable
   enabled=1
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-stable-debuginfo]
   name=Docker CE Stable - Debuginfo $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/debug-$basearch/stable
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-stable-source]
   name=Docker CE Stable - Sources
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/source/stable
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-edge]
   name=Docker CE Edge - $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/$basearch/edge
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-edge-debuginfo]
   name=Docker CE Edge - Debuginfo $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/debug-$basearch/edge
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-edge-source]
   name=Docker CE Edge - Sources
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/source/edge
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-test]
   name=Docker CE Test - $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/$basearch/test
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-test-debuginfo]
   name=Docker CE Test - Debuginfo $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/debug-$basearch/test
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-test-source]
   name=Docker CE Test - Sources
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/source/test
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-nightly]
   name=Docker CE Nightly - $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/$basearch/nightly
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-nightly-debuginfo]
   name=Docker CE Nightly - Debuginfo $basearch
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/debug-$basearch/nightly
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
    
   [docker-ce-nightly-source]
   name=Docker CE Nightly - Sources
   baseurl=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/7/source/nightly
   enabled=0
   gpgcheck=1
   gpgkey=https://mirrors.ustc.edu.cn/docker-ce/linux/centos/gpg
   ```

4. 问题：`sudo yum install docker-ce`提示如下

   ```
   Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
   ```

   解决：

   ```bash
   yum provides '*/applydeltarpm'
   yum install deltarpm
   ```

5. 问题`docker structure needs cleaning`

   解决：`docker system prune -a`



