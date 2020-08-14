---
title: WSL-install-java
date: 2019-02-14 17:45:05
updated: 2019-02-14 19:47:53
categories: WSL
tags: [java,tomcat]
---

#### win10子系统Ubuntu安装java

##### 安装java环境

```bash
cd /usr/lib/
sudo mkdir jvm
#在windos下载的该文件路径
sudo mv jdk-8u201-linux-x64.tar.gz /usr/lib/jvm/
#在/usr/lib/jvm路面
sudo tar -zxvf jdk-8u201-linux-x64.tar.gz
sudo rm jdk-8u201-linux-x64.tar.gz
```

##### 配置环境变量

`sudo vim ~/.bashrc`在文件末尾添加

```properties
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_201
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```

执行`source ~/.bashrc`生效配置

测试`java -version`

#### 运行tomcat

进入tomcat安装目录，windos和linux通用，然后右键打开ubunt，执行`./catalina.sh run`



### 注意事项

tomcat不要放`Program Files`带空格或特殊字符的路径，在linux下识别不了



