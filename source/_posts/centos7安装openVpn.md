---
title: centos7安装openVpn
date: 2017-09-20 23:13:37
categories: centos
tags: [centos,OpneVpn]
---
###  centos7安装openVpn

```shell
#安装依赖的软件包
yum install -y lzo lzo-devel openssl openssl-devel pam pam-devel
yum install -y pkcs11-helper pkcs11-helper-devel
#确认已经安装完成
rpm -qa lzolzo-devel openssl openssl-devel pam pam-devel pkcs11-helper pkcs11-helper-devel
#下载 openvpn 的源码包
wget http://oss.aliyuncs.com/aliyunecs/openvpn-2.2.2.tar.gz 
#安装 rpm 包工具和依赖项
yum install rpmdevtools pcre-devel gcc make
#生成 rpm build 目录树
rpmdev-setuptree
#使用 rpmbuild 将源码包编译成rpm包来进行安装
rpmbuild -tb openvpn-2.2.2.tar.gz 
#编译完成以后会在 /root/rpmbuild/RPMS/x86_64 目录下生成openvpn-2.2.2-1.x86_64.rpm
以rpm包的方式安装
rpm -ivh openvpn-2.2.2-1.x86_64.rpm
#初始化 PKI
cd /usr/share/doc/openvpn-2.2.2/easy-rsa/2.0
```

编辑vars证书`vim vars`

```properties
#所在的国家
export KEY_COUNTRY="CN"
#所在的省份
export KEY_PROVINCE="GD"
#所在的城市
export KEY_CITY="GuangZhou"
#所属组织
export KEY_ORG="xuan"
#邮件地址
export KEY_EMAIL=xuan.fong1@163.com
```

```shell
# 做个软链接到openssl-1.0.0.cnf配置文件 
ln -s openssl-1.0.0.cnf openssl.cnf
source ./vars
#清除并删除 keys 目录下的所有 key 
./clean-all
#生成 CA 证书，刚刚已经在 vars 文件中配置了默认参数值，多次回车完成就可以
./build-ca 
#生成服务器证书，其中 aliyuntest 是自定义的名字，一直回车，到最后会有两次交互，输入 y 确认，完成后会在 keys 目录下保存了 aliyuntest.key、aliyuntest.csr 和 aliyuntest.crt 三个文件
./build-key-server aliyuntest
#创建用户秘钥与证书 创建用户名为 aliyunuser 的秘钥和证书，一直回车，到最后会有两次确认，只要按y确认即可。完成后，在 keys 目录下生成 1024 位 RSA 服务器密钥 aliyunuser.key、aliyunuser.crt 和 aliyunuser.csr 三个文件。
./build-key aliyunuser
#生成 Diffie Hellman参 数  执行了./build-dh后，会在 keys 目录下生成 dh 参数文件 dh1024.pem。该文件客户端验证的时候会用到。  
./build-dh
#将 /usr/share/doc/openvpn-2.2.2/easy-rsa/2.0/keys 目录下的所有文件复制到 /etc/openvpn下
cp -a /usr/share/doc/openvpn-2.2.2/easy-rsa/2.0/keys/*  /etc/openvpn/
#复制 openvpn 服务端配置文件 server.conf 到 /etc/openvpn/ 目录下
cp -a /usr/share/doc/openvpn-2.2.2/sample-config-files/server.conf  /etc/openvpn/
```

编辑配置server.conf文件`vim server.conf`

```properties
local 1.1.1.1  此处请填写用户自己的云服务器的公网IP地址
port 1194
proto udp
dev tun
ca ca.crt
cert aliyuntest.crt   此处crt以及下一行的key，请填写生成服务器端证书时用户自定义的名称
key aliyuntest.key  
dh dh1024.pem
server 172.16.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 223.5.5.5"  
client-to-client
keepalive 10 120
comp-lzo
user nobody
group nobody
persist-key
persist-tun
status openvpn-status.log
log         openvpn.log
verb 3
```

`egrep -v "^$|^#|^;" server.conf`查看配置文件，过滤功能

配置完成文件如下

```properties
local 112.74.51.136
port 1194
proto udp
dev tun
ca ca.crt
cert aliyuntest.crt
key aliyuntest.key  # This file should be kept secret
dh dh1024.pem
server 172.16.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 223.5.5.5"
client-to-client
keepalive 10 120
comp-lzo
user nobody
group nobody
persist-key
persist-tun
status openvpn-status.log
log         openvpn.log
verb 3
```

```
#直接关闭防火墙
systemctl stop firewalld.service
#禁止firewall开机启动
systemctl disable firewalld.service
#设置 iptables service
yum -y install iptables-services
```

如果要修改防火墙配置，如增加防火墙端口3306

`vi /etc/sysconfig/iptables `

在文件iptables添加如下内容

```properties
-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
```

最后重启系统使设置生效即可。

```shell
systemctl start iptables.service #打开防火墙
systemctl stop iptables.service #关闭防火墙
#重启防火墙
/etc/init.d/iptables restart 
#查看CentOS防火墙信息：
/etc/init.d/iptables status 
#检查是不是服务器的80端口被防火墙堵了
telnet server_ip 80
```

设置前请确保 iptables 已经开启，而且 /etc/sysconfig/iptables 文件已存在。然后开启转发：

`vi /etc/sysctl.conf`

添加如下内容

```properties
net.ipv4.ip_forward = 1
```

```shell
#然后使内核参数生效
sysctl -p
#添加 iptables 规则确保服务器可以转发数据包到阿里云内外网
iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -j MASQUERADE
#保存 iptables 配置
service iptables save
#启动 OpenVPN
/etc/init.d/openvpn start
#通过 netstat -ano | grep 1194 查看 1194 端口在监听，确保 openvpn 在运行中
netstat -ano | grep 1194
```

## #客户端

将 openvpn 安装路径下的 \OpenVPN\sample-config\ 目录中下的 client.opvn 复制到 openvpn 安装路径下的 \OpenVPN\config 目录，然后修配置文件中的如下参数； 

```
proto udp   去掉前面的分号，采用与服务器端相同的udp协议 
remote  1.1.1.1  1194   此处将1.1.1.1修改为用户的云服务器的公网IP地址，同时将该行前面的注释分号去掉
cert aliyunuser.crt     
key aliyunuser.key
```





##### 参考

 [云服务器 ECS Linux CentOS OpenVPN 配置概述](https://help.aliyun.com/knowledge_detail/42521.html)

[CentOS 7 从源码创建 RPM 包安装](https://blog.itnmg.net/2015/09/02/centos-7-build-rpm/)

[Centos 7和 Centos 6开放查看端口 防火墙关闭打开](http://www.cnblogs.com/eaglezb/p/6073739.html)