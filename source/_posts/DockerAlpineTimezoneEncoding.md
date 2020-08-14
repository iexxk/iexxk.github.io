---
title: Docker-Alpine-Timezone-Encoding
date: 2018-07-16 13:44:05
updated: 2018-12-12 10:47:58
categories: Docker
tags: [Docker,Alpine,Timezone,Encoding]
---

### 时区问题

alpine镜像默认时区是`UTC`,执行命令`date`可以进行查看时区，默认返回`Mon Jul 16 03:43:52 UTC 2018`,因此在查看日志，以及java代码里使用`new date()`时获取的时间时UTC格式的。

#### 原因

参考：[Setting the timezone](https://wiki.alpinelinux.org/wiki/Setting_the_timezone)

解决apline时区问题只需安装`tzdata`然后设置下就可以了,在alpine执行

添加字体的化安装`ttf-dejavu`解决


```verilog
java.lang.NullPointerException: null
at sun.awt.FontConfiguration.getVersion(FontConfiguration.java:1264)
```

```sh
date #查看时区UTC
apk update 
apk add tzdata ttf-dejavu
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
echo "Asia/Shanghai" > /etc/timezone
date #执行命令date可以进行查看时区
```

#### 解决方式一（采用）

镜像大小：

* java:8-jre-alpine 107.9M
* java:8-jre-alpine-cst  109.2M

封装docker镜像一层,这里操作的基础镜像是用`java:8-jre-alpine`进行封装

```dockerfile
# 生成镜像name:java:8-jre-alpine-cst
FROM java:8-jre-alpine
RUN  apk add --no-cache tzdata ttf-dejavu \
	&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
```

下次直接就直接使用自己的镜像`java:8-jre-alpine-cst`

参考：[Linux下修改时区](http://www.itfanr.cc/2017/02/23/modify-timezone/)

#### 解决方式二

可以直接封装在`java:8-jre-alpine`镜像里，这种需要知道`java:8-jre-alpine`镜像的[`dockerfile`](https://github.com/docker-library/openjdk/blob/9a0822673dffd3e5ba66f18a8547aa60faed6d08/8-jre/alpine/Dockerfile)于构建所需的环境包，这种方式构建镜像理论上应该比方式一小。

#### 解决方式三

在构建java应用程序时构建进行时区设置，这种方式存在，每次打包都要构建安装执行`tzdata`,在网差的情况下，这种构建就很慢了

```dockerfile
#基础镜像选择alpine 小巧安全流行方便
FROM java:8-jre-alpine
#复制固定路径下打包好的jar包(target/*.jar)并重命名到容器跟目录(/app.jar)，或ADD
COPY target/service.jar app.jar
COPY target/lib lib
RUN  apk add --no-cache tzdata \
	&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
#健康检查 -s 静默模式，不下载文件
#HEALTHCHECK CMD wget -s http://127.0.0.1:14030/actuator/health || exit 1
#启动容器执行的命令 java -jar app.jar ,如果加其他参数加 ,"-参数",
CMD ["java","-jar","app.jar"]
```

### debian 系统

```bash
#TZ=Asia/Shanghai
#命令行设置方法
ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone
```

##### dockerfile 设置

```dockerfile
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

