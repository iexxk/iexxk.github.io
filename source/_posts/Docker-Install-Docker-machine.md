---
title: Docker集群之Docker-machine安装
date: 2017-10-10 09:25:37
updated: 2018-12-12 10:47:58categories: Docker
tags: [集群,Swarm,docker,nginx,overlay,ingress]
---
### Docker-machine单独安装 (废弃)

###### 官网：[docker/machine](https://github.com/docker/machine)

##### 环境

* win10
* gitbash

#### 安装(On Windows with git bash)

```
$ if [[ ! -d "$HOME/bin" ]]; then mkdir -p "$HOME/bin"; fi && \
curl -L https://github.com/docker/machine/releases/download/v0.12.2/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe" && \
chmod +x "$HOME/bin/docker-machine.exe"
```

执行上面的命令半天下载不下来，可以手动下载https://github.com/docker/machine/releases/download/v0.12.2/docker-machine-Windows-x86_64.exe然后执行

```
if [[ ! -d "$HOME/bin" ]]; then mkdir -p "$HOME/bin"; fi && mv docker-machine-Windows-x86_64.exe $HOME/bin/docker-machine.exe && chmod +x "$HOME/bin/docker-machine.exe"
```

