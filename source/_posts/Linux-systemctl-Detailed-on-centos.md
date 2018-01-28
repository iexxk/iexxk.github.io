---
title: centos7 systemctl服务详解
date: 2017-12-05 13:56:37
updated: 2017-12-12 17:13:44categories: Linux
tags: [centos,systemd,service]
---
### 介绍

系统服务`/lib/systemd/system`

用户服务(需要登陆后才能执行)`/usr/lib/systemd/system`

Systemd服务文件以.service结尾

######注：ubuntu是在`/etc/systemd/system/`

### 常用命令

```sh
#查看所有启动的服务
systemctl list-units --type=service
#重启
systemctl restart nginx.service
#查看状态
systemctl status nginx.service
#启动
systemctl start nginx.service
#开机启动	
systemctl enable nginx.service
#关闭开机启动	
systemctl disable nginx.service
#重新扫描变动
systemctl daemon-reload
#查看所有的服务
systemctl list-unit-files
```

#### 配置文件解释

普通服务文件命名规则`serverName.service`

带参数服务文件命名规则`serverName@.service`,使用时`systemctl start serverName@%i`其中`%i`为动态参数，一般为配置文件名

```properties
[Unit] #服务说明
#描述
Description=Shadowsocks-Libev Custom Client Service for %I  
Documentation=man:ss-local(1)
#描述服务类别
After=network.target

[Service] #服务运行参数设置
#运行形式forking 后台形式、simple 普通模式？
Type=simple
#全局变量配置文件
#EnvironmentFile=/etc/sysconfig/shadowsocks-libev
# "$CONFFILE"配置在全局变量配置文件shadowsocks-libev，见附件
#ExecStart=/usr/bin/ss-local -c "$CONFFILE" $DAEMON_ARGS

CapabilityBoundingSet=CAP_NET_BIND_SERVICE
#服务的具体运行命令
ExecStart=/usr/bin/ss-local -c /etc/shadowsocks-libev/%i.json
#ExecReload=为重启命令
#ExecStop=为停止命令
User=nobody
Group=nobody
LimitNOFILE=32768

[Install]
WantedBy=multi-user.target
```

### 实战

### 残酷，革命尚未成功

`vim /usr/lib/systemd/system/dropbox.service`添加一个用户登陆后启动的服务

```properties
[Unit]
Description=Dropbox as a system service user

[Service]
Type=forking
ExecStart=/usr/bin/dropbox start
ExecStop=/usr/bin/dropbox stop
User=nobody
Group=nobody
# 'LANG' might be unnecessary, since systemd already sets the
# locale for all services according to "/etc/locale.conf".
# Run `systemctl show-environment` to make sure.
#Environment=LANG=en_US.utf-8

[Install]
WantedBy=multi-user.target
```







## 附件

`shadowsocks-libev`

```properties
START=yes
CONFFILE="/etc/shadowsocks-libev/config.json"
DAEMON_ARGS="-u"
USER=nobody
GROUP=nobody
MAXFD=32768    
```

