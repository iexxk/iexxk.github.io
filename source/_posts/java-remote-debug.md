---
title: Java-remote-debug
date: 2018-12-20 11:02:25
updated: 2018-12-20 11:35:24
categories: Java
tags: [Java,ieda,debug]
---

## idea远程debug总结

#### springboot

启动参数添加`-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005`

docker环境配置:

```dockerfile
CMD ["java","-jar","-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005","-Dspring.profiles.active=sit","app.jar"]
```

[idea springboot 远程调试模式之本地](https://jingyan.baidu.com/article/4ae03de3ca29393eff9e6b8d.html)
[idea基于springboot远程调试之docker环境](https://jingyan.baidu.com/article/6181c3e0d1f3a8152ef1538d.html)

#### tomcat

`catalina.sh`文件添加`CATALINA_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=5005,suspend=n,server=y"`

docker环境配置:

```dockerfile
    environment:
      CATALINA_OPTS: "-Xdebug -Xrunjdwp:transport=dt_socket,address=5005,suspend=n,server=y"
```



