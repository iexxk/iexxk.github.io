---
title: OpenVpn配置详解
date: 2017-11-22 14:13:37
updated: 2018-01-28 21:41:27categories: 网络
tags: [OpenVpn,网络,路由]
---

#### 路由

`route`或`route PRINT`

| Destination（ip/网段） | Gateway（网关） | Genmask（子网掩码）       | Iface(网卡) |
| ------------------ | ----------- | ------------------- | --------- |
| 192.168.123.110    | 10.8.0.2    | 255.255.255.255（ip） | tun0      |
| 192.168.123.0      | 10.8.0.1    | 255.255.255.0(网段)   | tun0      |

###### 解释

第一条：访问192.168.123.110将从tun0网卡的10.8.0.2的网关转发出去

第二条：访问192.168.(1~255)内所有的ip将从网卡tun0网卡的10.8.0.1的网关转发出去

#### 服务配置

```properties
#推送路由192.168.123.110（ip）到所有客户端
push "route 192.168.123.110 255.255.255.255"
#推送路由192.168.123.0(网段)到所有客户端(除了在ccd客户端配置了这是他的路由的客户端)
push "route 192.168.123.0 255.255.255.0"
#设置服务器的路由：访问192.110.10.1时从10.8.0.1（网关）访问，10.8.0.1不设置可以从route命令查看网关是
route 192.110.10.1 255.255.255.255 10.8.0.1
```







####客户端配置

服务端需要添加配置`client-config-dir ccd`指定客户端配置目录为ccd

配置文件名为直接客户端的名字没有.conf和任何后缀

```properties
#指定客户端ip为10.8.0.7
ifconfig-push 10.8.0.7 255.255.255.0
#标记这是我的子网，让我的子网也可以访问openvpn,另一个作用就是push路由时，不会推送该路由到该客户端
iroute 192.168.123.0 255.255.255.0
route 192.168.123.0 255.255.255.0
```





我的设置如下

10.8.0.1 服务器

10.8.0.8 家

10.8.0.5 工作

server.conf

```properties
port 1194
proto tcp
dev tun
sndbuf 0
rcvbuf 0
ca ca.crt
cert server.crt
key server.key
dh dh.pem
auth SHA512
tls-auth ta.key 0
topology subnet
server 10.8.0.0 255.255.255.0
#ifconfig-pool-persist ipp.txt
#push "redirect-gateway def1 bypass-dhcp"
#push "dhcp-option DNS 100.100.2.138"
#push "dhcp-option DNS 100.100.2.136"
push "route 10.8.0.0 255.255.255.0"
push "route 192.168.123.0 255.255.255.0"
route 192.168.123.0 255.255.255.0 10.8.0.8
client-config-dir ccd
client-to-client
keepalive 10 120
cipher AES-256-CBC
comp-lzo
user nobody
group nobody
persist-key
persist-tun
status openvpn-status.log
verb 3
crl-verify crl.pem
```

client

```properties
ifconfig-push 10.8.0.8 255.255.255.0
iroute 192.168.123.0 255.255.255.0
route 192.168.123.0 255.255.255.0
```

