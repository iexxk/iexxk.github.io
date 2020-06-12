---
title: Network-common-problem
date: 2018-09-20 09:34:27
updated: 2020-06-08 10:28:42
categories: 网络
tags: [Network,linux]
---

# mac 篇

### 常用命令

```bash
# 查看当前路由表
netstat -rn
----------------------------------------------------------------
Routing tables
Internet:
Destination        Gateway            Flags        Netif Expire
default            192.168.43.88      UGSc           en0
default            11.13.2.254        UGScI          en7
-----------------------------------------------------------------
#获取默认路由
route get 0.0.0.0
--------------------------------------------------------------------------------
   route to: default
destination: default
       mask: default
    gateway: 192.168.43.88
  interface: en0
      flags: <UP,GATEWAY,DONE,STATIC,PRCLONING>
 recvpipe  sendpipe  ssthresh  rtt,msec    rttvar  hopcount      mtu     expire
       0         0         0         0         0         0      1500         0
---------------------------------------------------------------------------------
#删除默认路由
sudo route -n delete default 192.168.43.88
#添加外网网关
sudo route add -net 0.0.0.0 192.168.43.88
#添加内网网关
sudo route add -net 11.8.129.0 11.13.2.254
```

# Linux 篇

### 常见命令

```bash
#和网络有关的配置文件 
/etc/resolv.conf 
#查看网关设置 
grep GATEWAY /etc/sysconfig/network-scripts/ifcfg* 
#增加网关: 
route add default gw 192.168.40.1 
#重启网络 
service network restart 
#查看DNS解析 
grep hosts /etc/nsswitch.conf
```

## 分析

### `traceroute <ip>`

网络测试、测量、管理、分析，[官网](https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-121-mainline/12778-ping-traceroute.html#traceroute)

#### ICMP错误信息分析：

`!H`    不能到达主机

`!N`    不能到达网络

`!P`     不能到达的协议

`!S`     源路由失效

`!F`     需要分段

正常情况：

```sh
[root@environment-test1 ~]# traceroute 4.2.2.2
traceroute to 4.2.2.2 (4.2.2.2), 30 hops max, 60 byte packets
 1  gateway (192.168.1.1)  0.440 ms  0.594 ms  0.743 ms
 2  * * *
 3  121.33.196.105 (121.33.196.105)  4.352 ms  4.443 ms  4.521 ms
 4  183.56.31.37 (183.56.31.37)  7.290 ms 183.56.31.21 (183.56.31.21)  9.217 ms 183.56.31.13 (183.56.31.13)  6.755 ms
 5  153.176.37.59.broad.dg.gd.dynamic.163data.com.cn (59.37.176.153)  6.884 ms  6.993 ms  7.084 ms
 6  121.8.223.13 (121.8.223.13)  9.307 ms  5.848 ms 183.56.31.173 (183.56.31.173)  4.443 ms
 7  202.97.94.130 (202.97.94.130)  4.029 ms  4.165 ms 202.97.94.142 (202.97.94.142)  5.546 ms
 8  202.97.94.98 (202.97.94.98)  11.225 ms 202.97.94.118 (202.97.94.118)  6.177 ms  6.600 ms
 9  202.97.52.18 (202.97.52.18)  209.571 ms 202.97.52.142 (202.97.52.142)  206.772 ms 202.97.58.2 (202.97.58.2)  197.316 ms
10  195.50.126.217 (195.50.126.217)  213.784 ms  213.917 ms  211.676 ms
11  4.69.163.22 (4.69.163.22)  312.436 ms 4.69.141.230 (4.69.141.230)  214.040 ms  213.168 ms
12  b.resolvers.Level3.net (4.2.2.2)  209.348 ms  210.701 ms  210.588 ms
```

有问题的情况：

```sh
[root@lfadmin ~]# traceroute 4.2.2.2
traceroute to 4.2.2.2 (4.2.2.2), 30 hops max, 60 byte packets
 1  gateway (192.168.1.1)  0.751 ms !N  0.817 ms !N  1.326 ms !N
```

### `ifconfig <网卡名字>`



### `netstat -r`相似`route`

显示路由连接信息等

```sh
[root@environment-test1 ~]# netstat -r
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         gateway         0.0.0.0         UG        0 0          0 enp3s0
link-local      0.0.0.0         255.255.0.0     U         0 0          0 enp3s0
172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
172.18.0.0      0.0.0.0         255.255.0.0     U         0 0          0 doc...ridge
192.168.1.0     0.0.0.0         255.255.255.0   U         0 0          0 enp3s0
```



### `host <域名>` 相似`nslookup <域名>`

dns分析

```sh
[root@environment-test1 ~]#  host www.baidu.com
www.baidu.com is an alias for www.a.shifen.com.
www.a.shifen.com has address 14.215.177.38
www.a.shifen.com has address 14.215.177.39
```

### `nmcli`查看设备状态

`ip route show | column -t` 查看路由



### 问题1 ：无法连外网，可以ping 路由器

提示

```bash
[root@lfadmin ~]# traceroute 4.2.2.2
traceroute to 4.2.2.2 (4.2.2.2), 30 hops max, 60 byte packets
 1  gateway (192.168.1.1)  0.751 ms !N  0.817 ms !N  1.326 ms !N
```

解决原因，是网络配置文件uuid冲突，导致不能上网，修改即可

执行`uuidgen ens33`生产新的`830a6ae2-85fb-41e7-9e5d-60d084f56f5f`替换配置文件里面的

执行`nmcli con | sed -n '1,2p'`进行验证



### 参考

[CentOS7配置网卡为静态IP，如果你还学不会那真的没有办法了！](https://segmentfault.com/a/1190000011954814)



