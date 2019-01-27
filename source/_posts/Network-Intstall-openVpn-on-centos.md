---
title: centos7.4安装openVpn
date: 2017-10-12 14:13:37
updated: 2019-01-26 16:58:16
categories: 网络
tags: [centos,openVpn]
---

#### openvpn service安装与配置

##### 1.下载脚本`wget https://git.io/vpn -O openvpn-install.sh`


```sh
#添加执行权限
chmod +x openvpn-install.sh
#总结
wget https://git.io/vpn -O openvpn-install.sh && bash openvpn-install.sh
```

##### 2.运行脚本`./openvpn-install.sh`,设置如下

1. 监听地址设置为空 IP address: 
2. Protocol:[2]TCP
3. Port:1194
4. 不选DNS:
5. client name: client_k2
6. External IP : 112.74.51.136

##### 3. 配置服务端`vim /etc/openvpn/server.conf`

```properties
#指定ip,所以记录ip没效果屏蔽
;ifconfig-pool-persist ipp.txt
;push "redirect-gateway def1 bypass-dhcp"
#推送服务器路由
push "route 10.14.0.0 255.255.255.0"
#推送k2客户端子网路由到所有客户端除了ccd里面申明了该路由的客户端
push "route 192.168.123.0 255.255.255.0"
#添加服务器路由，访问客户端K2的192.168.123.0子网通过网关10.14.0.2(k2客户端ip)
route 192.168.123.0 255.255.255.0 10.14.0.2
#添加客户端配置目录，启用之后，每个客户端必须指定ip，否正有可能访问不了其他客户端的子网
client-config-dir ccd
#客户端访问客户端
client-to-client
```

##### 4. 配置客户端路由`mkdir /etc/openvpn/ccd`和`vim /etc/openvpn/ccd/client_k2`

```properties
#设置该客户端的vpn的ip是10.14.0.2,子网掩码必须是255.255.255.0，如果启用ccd，必须配置
ifconfig-push 10.14.0.2 255.255.255.0
#申明192.168.123.0是自己的子网，并且让子网也可以访问vpn服务器，申明之后不会推送该路由到该客户端
iroute 192.168.123.0 255.255.255.0
route 192.168.123.0 255.255.255.0
```

##### 5.添加客户端`./openvpn-install.sh`

1. Select an option[1-4]:1 (add a new user)
2. client name: client_worker

```sh
#编辑配置文件
vim /etc/openvpn/server.conf
#重启生效
systemctl restart openvpn@server.service
systemctl enable openvpn@server.service
#注释掉客户端的
#setenv opt block-outside-dns
```

##### 6.下载ovpn文件，并修改配置，注释调`#setenv opt block-outside-dns`

##### 7.常用命令

```sh
#重启生效
systemctl restart openvpn@server.service
#使能服务
systemctl enable openvpn@server.service
#ssh下载文件
scp root@112.74.51.136:/root/client_xuan_ubuntu.ovpn ./
```

#### openvpn client 安装与配置

#####  1.安装

```sh
yum update #更新
yum install vim  #安装vim
yum install epel-release  #添加epel源
yum clean all # 可选
yum update # 可选
yum makecache # 可选
yum install openvpn iptables-services #安装openvpn
scp root@112.74.51.136:~/client_vm.ovpn /etc/openvpn/client/ #下载客户端配置
#注释掉客户端的vim /etc/openvpn/client/client_vm.ovpn
#setenv opt block-outside-dns
#-----------------------废弃------------------------------------------------
openvpn --daemon --cd /etc/openvpn/client --config client_vm.ovpn --log-append /etc/openvpn/openvpn.log #启动
tail -100f /etc/openvpn/openvpn.log  #查看日志
ps -ef | grep openvpn #查看openvpn进程
kill <pid> #杀死进程
#---------------------废弃结束------------------------------------------------------
#openvpn-client启动服务，反斜杠转义字符，实际名称是openvpn-client@.service
vim /lib/systemd/system/openvpn-client\@.service
#修改
ExecStart=/usr/sbin/openvpn --suppress-timestamps --nobind --config %i.conf
#为
ExecStart=/usr/sbin/openvpn --daemon --config %i.ovpn --log-append /etc/openvpn/openvpn.log
#防止已经启动，@符号后面等效与%i,所以这里为客户端配置的名字
systemctl restart openvpn-client@client_vm
#开机启动
systemctl enable openvpn-client@client_vm
```

#### openvpn 服务端的局域网远程访问

#### 准备工作，安装iptables

It is possible to go back to a more classic iptables setup. First, stop and mask the firewalld service:

```
systemctl stop firewalld
systemctl mask firewalld
```

Then, install the iptables-services package:

```
yum install iptables-services
```

Enable the service at boot-time:

```
systemctl enable iptables
```

Managing the service

```
systemctl [stop|start|restart] iptables
```

Saving your firewall rules can be done as follows:

```
service iptables save
```

添加路由

```bash
iptables -t nat -A POSTROUTING -s 10.14.208.0/24 -j SNAT --to-source  192.168.1.230
service iptables save
```

`vim /etc/openvpn/server.conf ` 添加

```properties
push "route 192.168.1.0 255.255.255.0"
```



### 腾讯云openvpn服务器所在内网供openvpn客户端访问

```bash
# 10.34.0.0为openvpn网段
sudo iptables -t nat -A POSTROUTING -s 10.34.0.0/24 -o eth0 -j MASQUERADE
#查看规则
sudo iptables -nL -t nat
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match src-type LOCAL
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0           
MASQUERADE  all  --  172.18.0.0/16        0.0.0.0/0           
MASQUERADE  tcp  --  172.18.0.11          172.18.0.11          tcp dpt:3306
MASQUERADE  all  --  10.34.0.0            0.0.0.0/0  
#这句是新加的
MASQUERADE  all  --  10.34.0.0/24         0.0.0.0/0    
```







[openvpn tun模式下客户端与内网机器通信](https://shiguanghui.iteye.com/blog/2323327)

[iptables规则的查看和清除](http://cakin24.iteye.com/blog/2339362)

[iptables 添加，删除，查看，修改](http://blog.51yip.com/linux/1404.html)

[How can i use iptables on centos 7?](https://stackoverflow.com/questions/24756240/how-can-i-use-iptables-on-centos-7)

[使用openvpn实现访问远程网络](https://www.cnblogs.com/huangweimin/articles/7638943.html)

#### 参考

[官网](https://openvpn.net/index.php/open-source/documentation/howto.html#examples)

[脚本github官网Nyr/openvpn-install](https://github.com/Nyr/openvpn-install)

[openvpn的一个一键安装脚本“openvpn-install”让openvpn重放光彩，又可用openvpn翻墙了](https://groups.google.com/forum/#!topic/fqlt/GUn-QNO1ZpU)

[[How to Configure OpenVPN Server on CentOS 7.3](http://gamblisfx.com/configure-openvpn-server-centos-7-3/)](http://gamblisfx.com/configure-openvpn-server-centos-7-3/)

[使用 OpenVPN 互联多地机房及Dokcer跨主机/机房通讯](https://www.lsproc.com/post/routing-multiple-networks-and-dockers-through-openvpn)

[扩大OpenVPN使用范围，包含服务器或客户端子网中的其他计算机](http://www.softown.cn/post/151.html)