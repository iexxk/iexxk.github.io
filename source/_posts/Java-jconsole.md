---
 title: Java-jconsole
date: 2020-05-27 15:13:18
updated: 2020-05-27 15:34:11
categories: Java 
tags: [Java,jvm,springboot]
---

## springboot 配置jconsole

1. 设置远程连接访问密码

```bash
# 查看java安装目录
echo $PATH
# 切换到java安装目录
cd /usr/local/jvm/jdk1.8.0_77/jre/lib/management
# 创建一个密码文件
cp jmxremote.password.template jmxremote.password
# 添加文件可写权限
chmod +x jmxremote.password
# 取消最后两行注释 monitorRole  QED  和controlRole   R&D
vim jmxremote.password
# 修改文件权限为400或600解决启动`错误: 必须限制口令文件读取访问`
chmod 400 jmxremote.password
```

2. 修改启动命令，启动springboot

```bash
#方式一
##环境变量
JAVA_OPTS='-Djava.rmi.server.hostname=当前服务器公网ip 
-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=8888 
-Dcom.sun.management.jmxremote.rmi.port=8888 
-Dcom.sun.management.jmxremote.authenticate=true 
-Dcom.sun.management.jmxremote.ssl=false'
##启动命令
java $JAVA_OPTS -jar springboot.jar
#方式二 直接在启动命令里面加，不通过环境变量
java Djava.rmi.server.hostname=当前服务器公网ip 
-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=8888 
-Dcom.sun.management.jmxremote.rmi.port=8888 
-Dcom.sun.management.jmxremote.authenticate=true 
-Dcom.sun.management.jmxremote.ssl=false
-jar springboot.jar
```

3. 在本地启动jconsole

   终端里面执行`jconsole`就会打开jconsole

   然后选择远程连接，输入ip:端口 eg:10.10.10.11:8888然后输入用户名(monitorRole)和密码(QED)或者用户名：controlRole密码：R&D

   

#### 参考

[基于Springboot项目使用jconsole远程监控JVM](https://blog.csdn.net/Box_clf/article/details/88344631)

[Linux 错误: 必须限制口令文件读取访问: /sy/java/jdk1.6.0_26/jre/lib/management/jmxremote.password](https://blog.csdn.net/yejin191258966/article/details/100097592)

