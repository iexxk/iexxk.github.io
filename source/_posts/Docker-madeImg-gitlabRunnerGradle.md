---
title: Docker 制作 gitlabRunner+gradle镜像
date: 2018-01-17 23:40:37
updated: 2018-01-18 13:47:39categories: Docker
tags: [docker,gitlab,runner,gradle,java]
---
### gitlabRunner 镜像

[gitlab/gitlab-runner:latest]()

### 安装java环境

1. 下载jre,jre只是运行环境jdk包括jre还有编译环境

   [server-jre-8u161-linux-x64.tar.gz](http://www.oracle.com/technetwork/java/javase/downloads/index.html)

2. 移动文件到挂载卷`sudo mv server-jre-8u161-linux-x64.tar.gz  /var/lib/docker/volumes/gitLabRuner_home/_data`

3. 进入gitlab-runner 容器`sudo docker exec -it <容器id> bash`

4. 进入挂载目录`cd /home/gitlab-runner/`

5. 解压文件`tar zxvf server-jre-8u161-linux-x64.tar.gz`

6. 创建目录` `然后移动文件并重命名`mkdir /usr/lib/jvm && mv jdk1.8.0_161 /usr/lib/jvm/java-8-oracle`

7. 添加环境变量配置文件`vim /etc/profile.d/jdk.sh`然后再添加执行权限`chmod +x /etc/profile.d/jdk.sh`

   ```sh
   export J2SDKDIR=/usr/lib/jvm/java-8-oracle
   export J2REDIR=/usr/lib/jvm/java-8-oracle/jre
   export PATH=$PATH:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
   export JAVA_HOME=/usr/lib/jvm/java-8-oracle
   export DERBY_HOME=/usr/lib/jvm/java-8-oracle/db
   ```

8. 运行脚本使环境变量生效`source /etc/profile`

9. 测试`echo $JAVA_HOME`输出`/usr/lib/jvm/java-8-oracle`或者`java -version`

### 安装Gradle环境

1. 下载[gradle-4.4.1-bin.zip](https://gradle.org/releases/)

2. 移动文件到挂载卷`sudo mv gradle-4.4.1-bin.zip /var/lib/docker/volumes/gitLabRuner_home/_data/`

3. 解压`unzip /var/lib/docker/volumes/gitLabRuner_home/_data/gradle-4.4.1-bin.zip`

4. 进入gitlab-runner 容器`sudo docker exec -it <容器id> bash`

5. 进入挂载目录`cd /home/gitlab-runner/`

6. 移动目录`mv gradle-4.4.1 /usr/lib/gradle `

7. `vim /etc/profile.d/gradle.sh`并添加执行权限``

   ```sh
   export GRADLE_HOME=/usr/lib/gradle 
   export PATH=$GRADLE_HOME/bin:$PATH
   ```

8. 运行脚本使环境变量生效`source /etc/profile`

9. 测试`gradle -version`

### 制作镜像

1. 清理安装包
2. 清理命令历史`history -c`
3. `ctrl+p+q`退出容器不留记录 
4. `sudo docker commit -m "add java gradle" -a "iexxk" db38 exxk/gitlab-runner-gradle:v1.0`



### 问题

1. 通过exec命令进入容器后执行`source /etc/profile`生效环境变量，再次进入就没有该变量了，commit制作的镜像也没有生效环境变量

   解决：1.通过启动容器时设置环境变量或执行命令，再commit保存，不采用因为每一次提交都会使镜像变大，且是黑盒不易维护

### 总结

通过commit方法制作镜像会成为黑盒，且不容易维护，而且没提交一次，都会增大镜像的容量，因此采用dockerfile的形式制作镜像， commit适合用于保存犯罪现场。

##### 对应操作记录[docker通过commit制作带Gradle和java环境的镜像](https://jingyan.baidu.com/article/af9f5a2d704e6343140a45e6.html)