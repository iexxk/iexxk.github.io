---
title: frp内网穿透
date: 2017-09-07 09:39:38
updated: 2017-12-13 12:06:35categories: 网络
tags: [frp,集群,网络代理,局域网远程访问]
---
# fatedier[/frp](https://github.com/fatedier/frp)

frp 是一个可用于内网穿透的高性能的反向代理应用，支持 tcp, udp, http, https 协议。

### 搭建一个远程访问内网的web应用

frps 服务端程序(配置文件frps.ini)，放到公网ip的机器上（阿里云）

frpc 客户端程序(配置文件frpc.ini)，放到内网环境机器上（win10）

##### 法一     通过域名访问内网web服务

###### frps 服务端设置

```properties
# frps.ini
[common]
#frps服务端口
bind_port = 7000
#web远程访问端口
vhost_http_port = 10080
#https使用这个
#vhost_https_port = 8080
```

启动服务端`./frps -c ./frps.ini`

###### frpc 客户端设置

```properties
# frpc.ini
[common]
#服务器公网ip
server_addr = 112.74.51.136
#frps 服务端口和服务端对应
server_port = 7000

[web]
#web服务网络类型，可选http、https
type = http
#内网机器的web服务端口
local_port = 8080
#配置域名(必须绑定域名)
custom_domains = exxk.me
```

启动客户端`.\frpc.exe -c .\frpc.ini`

##### 法二     通过ssh(IP)访问内网web服务

###### frps 服务端设置

```properties
# frps.ini
[common]
#frps服务端口
bind_port = 7000
```

启动服务端`./frps -c ./frps.ini`

###### frpc 客户端设置

```properties
# frpc.ini
[common]
#服务器公网ip
server_addr = 112.74.51.136
#frps 服务端口和服务端对应
server_port = 7000

[ssh]
type = tcp
#web服务本地访问地址
local_ip = 127.0.0.1
#web服务本地访问端口
local_port = 8080
#远程调用web服务时的端口
remote_port = 10080
```

启动客户端`.\frpc.exe -c .\frpc.ini`

