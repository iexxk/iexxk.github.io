---
title: redis集群搭建
date: 2019-01-22 22:06:32
updated: 2019-07-31 13:49:21
categories: 数据库
tags: [redis]
---



### 安装ruby

```bash
#依赖环境
yum -y install gcc automake autoconf libtool make
#安装源
yum install centos-release-scl-rh
#安装ruby2.3
yum install rh-ruby23 -y
#使能ruby2.3（每次要重新执行）
scl enable rh-ruby23 bash
#查看版本2.3
ruby -v
```

### 安装[redis](http://download.redis.io/releases/)

```bash
yum install wget
wget http://download.redis.io/releases/redis-3.2.6.tar.gz
tar xzf redis-3.2.6.tar.gz
mv redis-3.2.6 /opt/redis
make
#运行测试
/opt/redis/src/redis-server /opt/redis/redis.conf
# 使用redis-trib集群需要执行
gem install redis 
# 创建集群
./src/redis-trib.rb create --replicas 1 192.168.101.108:7000 192.168.101.108:7001 192.168.101.108:7002
```

### docker方式构建

部署脚本：

```dockerfile
  redis700x:
    image: redis
    restart: always
    hostname: redis-master
    command: "redis-server /data/redis.conf"
    volumes:
      - /dockerdata/v-yinfu/redis/7000:/data
    ports:
      - target: 700x
        published: 700x
        protocol: tcp
        mode: host
      - target: 1700x
        published: 1700x
        protocol: tcp
        mode: host  
```

配置文件：

```properties
## 自定义配置
# redis:3.2.6需要打开
# bind 0.0.0.0
protected-mode no
port 700x
# cluster-announce-x系列参数redis:5-alpine才支持，3.2.6屏蔽
cluster-announce-port 700x
cluster-announce-bus-port 1700x
# 自己服务器的ip
cluster-announce-ip 192.168.101.108
daemonize no
appendonly yes
cluster-enabled yes
appendonly yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
```

上面x换成0-6

```bash
# 创建集群
./redis-trib.rb create --replicas 1 192.168.101.108:7000 192.168.101.108:7001 192.168.101.108:7002 192.168.101.108:7003 192.168.101.108:7004 192.168.101.108:7005
# 检查集群
./src/redis-trib.rb check 192.168.101.108:7000
```

### 使用docker镜像脚本创建

```bash
#创建集群 主1 主2 主3 从1 从2 从3 的顺序来的
docker run -it --rm exxk/redis-trib ruby redis-trib.rb create --replicas 1 172.16.16.8:7000 172.16.16.8:7001 172.16.16.8:7002 172.16.16.13:7003 172.16.16.13:7004 172.16.16.13:7005
#检查集群状态
docker run -it --rm exxk/redis-trib ruby redis-trib.rb check 192.168.101.108:7000
# 查看集群负载
docker stats $(docker ps | grep "redis-cluster" | awk '{ print $1 }')
# 修复集群
docker run -it --rm exxk/redis-trib ruby redis-trib.rb fix 10.10.10.11:7000
```

## 高可用总结

1. 执行集群creat脚本时，默认前三个为主后三个为从，主从对应关系随机分配
2. 集群存在主从对应关系，一个主回自动分配一个从，集群宕机也不会改变
3. 集群一个主从挂了不能访问
4. 集群必须所有的主都能正常运行
5. 集群从升级主存在时间间隔，试配置和性能等因素影响，可能长可能短，在没有主选择成功集群状态显示异常，且无法访问，提示错误`Not all 16384 slots are covered by nodes.`
6. 集群同时宕机两个主，从是无法升级为主，这种情况只在同时，如果其中一个从升级主，再宕机一个主，是没有关系的
7. 从节点宕机对主节点毫无影响

### 常见问题

问题1： 一直提示waiting  for

```
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join..
```

解决：防火墙开端口

```bash
# 添加端口7000-7005/17000-17005
firewall-cmd --zone=public --add-port=7000/tcp --permanent
# 重载配置
firewall-cmd --reload
# 检查防火墙规则
firewall-cmd --list-all
# ports: 7000/tcp 7001/tcp 7002/tcp 7003/tcp 7004/tcp 7005/tcp 17005/tcp 17004/tcp 17003/tcp 17002/tcp 17001/tcp 17000/tcp
# 查看防火墙状态
firewall-cmd --state
# 临时关闭防火墙,重启后会重新自动打开
systemctl restart firewalld
```

然后删除服务及缓存文件重新启动

```bash
# 删除缓存文件
rm -f /dockerdata/v-yinfu/redis/700*/appendonly.aof
rm -f /dockerdata/v-yinfu/redis/700*/nodes.conf 
# 重新集群
./redis-trib.rb create --replicas 1 192.168.101.108:7000 192.168.101.108:7001 192.168.101.108:7002 192.168.101.108:7003 192.168.101.108:7004 192.168.101.108:7005
```

问题2 版本兼容问题

redis5 不支持jedis2.8，会提示错误`7001@17001`，升级jedis3.0可以解决

redis5(4)一下不支持docker 集群模式

```
cluster-announce-port 700x
cluster-announce-bus-port 1700x
# 自己服务器的ip
cluster-announce-ip 192.168.101.108
```







## 参考

[docker redis 集群（cluster）搭建](https://my.oschina.net/dslcode/blog/1936656)

[centos7安装redis4集群服务](https://my.oschina.net/zhaoqian/blog/1793063)

官网：[https://redis.io/documentation](https://link.jianshu.com/?t=https%3A%2F%2Fredis.io%2Fdocumentation)
中文官网：[http://www.redis.cn/documentation.html](https://link.jianshu.com/?t=http%3A%2F%2Fwww.redis.cn%2Fdocumentation.html)