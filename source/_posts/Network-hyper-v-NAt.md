---
title: Network-hyper-v-NAt
date: 2018-04-19 22:05:50
updated: 2018-04-25 20:47:32
categories: 网络
tags: [Network,static,NAT,hyper-v]
---

## hyper-v设置静态ip

#### 创建NAT网络

用管理员权限运行`powershell`,下面命令会创建一个NAT内部网络，网段为`192.168.204.0/24`，可以在网络适配器可以找到新建的`NAT-Docker`网络适配器

```powershell
#创建新的虚拟交换机NAT-Docker
New-VMSwitch –SwitchName "NAT-Docker" –SwitchType Internal –Verbose
#查看所有网路适配器，找到对应ifIndex 值
Get-NetAdapter
#新建一个NAT网关192.168.204.181，注意替换InterfaceIndex为ifIndex值
New-NetIPAddress –IPAddress 192.168.204.1 -PrefixLength 24 -InterfaceIndex 37 –Verbose
#创建一个nat网络
New-NetNat –Name NATNetwork –InternalIPInterfaceAddressPrefix 192.168.204.0/24 –Verbose
```

#### 配置NAT网络

在新建的网络适配器`NAT-Docker`设置固定ip为`192.168.204.1`,dns记得也要设置`202.96.128.86`根据自己实际情况设置dns

在hyper-v虚拟机里切换centos使用该网络

#### centos配置静态ip

在centos修改网络配置文件`vim /etc/sysconfig/network-scripts/ifcfg-eth0 `

```properties
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
#BOOTPROTO="dhcp"
BOOTPROTO="static"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="eth0"
UUID="d49f62d7-9c2a-4f6f-8077-605d0dd65eea"
DEVICE="eth0"
ONBOOT="yes"
#---以下新加
NM_CONTROLLED="no"
IPADDR="192.168.204.181"
NETMASK="255.255.255.0"
GATEWAY="192.168.204.1"
BROADCAST="192.168.204.255"
DNS1="8.8.8.8"
```

执行`service network restart`重启网络



#### 端口映射（需管理员权限）

![](http://ohdtoul5i.bkt.clouddn.com/1531476067353.png)

```powershell
#查询端口映射情况
netsh interface portproxy show v4tov4
#添加端口映射
netsh interface portproxy add v4tov4 listenport=外网端口 listenaddress=主IP connectaddress=私网IP connectport=私网IP端口
#eg
netsh interface portproxy add v4tov4 listenport=14014 listenaddress=192.168.1.158 connectaddress=192.168.204.182 connectport=14014
#删除一个端口映射
netsh interface portproxy delete v4tov4 listenaddress=主IP listenport=外网端口
#eg
netsh interface portproxy delete v4tov4 listenaddress=192.168.1.158 listenport=14014
```

![](http://ohdtoul5i.bkt.clouddn.com/1531475386029.png)

参考[Hyper-V 共享式网络链接 端口映射](https://my.oschina.net/alongite/blog/1537054)