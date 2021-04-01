---
title: Docker-SpringBoot
date: 2021-03-25 16:50:09
updated: 2021-03-26 09:34:43
categories: Docker
tags: [SpringBoot]
---



```dockerfile
#基础镜像选择alpine 小巧安全流行方便
FROM exxk/java:8-alpine-cst
# 暴露端口
EXPOSE 9303
# 设置参数
ARG JAVA_OPTS="-Xms256m -Xmx256m -XX:NewRatio=1"
#复制固定路径下打包好的jar包(target/*.jar)并重命名到容器跟目录(/app.jar)，或ADD
COPY target/*.jar app.jar
COPY src/main/resources/bootstrap.properties config/bootstrap.properties
#COPY target/lib lib
#健康检查 -s 静默模式，不下载文件
HEALTHCHECK --start-period=40s --interval=30s --timeout=5s --retries=5 CMD (wget http://localhost:9303/actuator/health -q -O -) | grep UP || exit 1
#启动容器执行的命令 java -jar app.jar ,如果加其他参数加 ,"-参数",
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app.jar"]
```



```bash
HEALTHCHECK --start-period=40s --interval=30s --timeout=5s --retries=5 CMD (wget http://localhost:9303/actuator/health -q -O -) | grep UP || exit 1
HEALTHCHECK [OPTIONS] CMD command 通过运行容器内的一个指令来检查容器的健康情况
--interval=DURATION 间隔时间， 默认 30s （30秒）;
--timeout=DURATION 超时时间， 默认 30s （30秒）;
#为需要启动的容器提供了初始化的时间段， 在这个时间段内如果检查失败， 则不会记录失败次数。 如果在启动时间内成功执行了健康检查， 则容器将被视为已经启动， 如果在启动时间内再次出现检查失败， 则会记录失败次数。
--start-period=DURATION 启动时间， 默认 0s， 如果指定这个参数， 则必须大于 0s ；
--retries=N 重试次数， 默认 3 ；
#获取http://localhost:9303/actuator/health内容然后 通过管道｜ 在获取的内容里面找up，找到了代表执行成功，没找到代表执行失败， || 代表前面的命令执行成功就会执行后面的命令，如果前面执行失败，后面就不会执行
(wget http://localhost:9303/actuator/health -q -O -) | grep UP || exit 1
```

