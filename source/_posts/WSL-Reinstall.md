---
title: WSL重装win10的Ubuntu子系统
date: 2017-07-18 23:34:28
updated: 2019-02-22 16:22:02
categories: WSL
tags: [win10,ubuntu,WSL]
---

命令行

`lxrun`查看对LX子系统执行管理操作的帮助

`lxrun /install` 安装子系统

`lxrun /uninstall` 卸载子系统

`lxrun /setdefaultuser`配置子系统用户

`lxrun /update` 更新子系统的包索引



### [安装brew](http://linuxbrew.sh/)

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile
```



#### 参考

[Windows10 Ubuntu子系统的删除和重装](http://www.linuxdiyf.com/linux/24338.html)