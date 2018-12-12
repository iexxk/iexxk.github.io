---
title: Docker-Alpine
date: 2018-04-21 22:31:49
updated: 2018-04-22 01:15:24
categories: Docker
tags: [Docker,Alpine]
---

## Docker之基础系统Alpine Linux

Alpine是一个linux迷你系统，体积小、安全，docker中ubuntu的替代系统

* 小巧: 官方镜像[docker pull alpine](https://store.docker.com/images/alpine)只有4.15M
* 安全: 面向安全的轻量发行版
* 简单: 提供apk包管理工具从[仓库](https://pkgs.alpinelinux.org/packages)管理安装
* 容器的基础镜像

[gliderlabs/docker-alpine](https://github.com/gliderlabs/docker-alpine)

[文档Alpine](https://yeasy.gitbooks.io/docker_practice/content/cases/os/alpine.html)

#### 基本使用

去[Alpine仓库](https://pkgs.alpinelinux.org/packages)搜索你要安装的组件(package)然后执行`apk add --no-cache <Package name>`

#### docker 中alpine使用

```sh
docker run alpine echo '123' #输出123，运行完镜像即摧毁
docker run -it --name myalpine alpine #运行一个容器并进入
### alpine常用命令，apk --help
apk info #查看安装的apk
apk update #更新镜像列表
cat /etc/apk/repositories #查看源
#http://dl-cdn.alpinelinux.org/alpine/v3.7/main
#http://dl-cdn.alpinelinux.org/alpine/v3.7/community
echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories #添加测试源,记得apk update
cat /etc/apk/arch  #查看系统版本Architecture，修改之后，之后的安装包都以该修改后的为准
apk upgrade #升级系统软件，解决编译版本过低等问题
```

利用docker 构建mysql镜像

```
FROM alpine:3.5
RUN apk add --no-cache mysql-client
ENTRYPOINT ["mysql"]
```

构建opencv镜像

```
FROM alpine:3.5
RUN apk add --no-cache opencv
ENTRYPOINT ["opencv"]
```

### 参考

[Alpine Linux 使用简介](https://blog.csdn.net/csdn_duomaomao/article/details/76152416)

```sh
#采用国内阿里云的源，文件内容为：
cat > /etc/apk/repositories <<EOF
https://mirrors.aliyun.com/alpine/v3.7/main/
https://mirrors.aliyun.com/alpine/v3.7/community/
https://mirrors.aliyun.com/alpine/edge/testing/
EOF
# 如果采用中国科技大学的源，文件内容为：
https://mirrors.ustc.edu.cn/alpine/v3.6/main/
https://mirrors.ustc.edu.cn/alpine/v3.6/community/
https://mirrors.ustc.edu.cn/alpine/edge/testing/
```





