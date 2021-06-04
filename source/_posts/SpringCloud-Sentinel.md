---
title: SpringCloud-Sentinel
date: 2021-06-04 13:39:10
updated: 2021-06-04 13:51:28
categories: SpringCloud
tags: [SpringCloud,Sentinel]
---

## 服务熔断与降级

### Sentinel 熔断与降级

主要功能：实时监控、机器发现、规则配置

### Sentinel控制台安装

[alibaba](https://github.com/alibaba)/**[Sentinel](https://github.com/alibaba/Sentinel)**

[ruoyi-cloud/sentinel](http://doc.ruoyi.vip/ruoyi-cloud/cloud/sentinel.html#%E5%9F%BA%E6%9C%AC%E4%BB%8B%E7%BB%8D)

#### Docker 镜像构造[iexxk](https://github.com/iexxk)/**[dockerbuild-Sentinel](https://github.com/iexxk/dockerbuild-Sentinel)**

```dockerfile
#基础镜像选择alpine 小巧安全流行方便
FROM exxk/java:8-alpine-cst
#apk安装完整wget，才能下载ssl的包，下载官方的安装包
RUN apk add --no-cache wget && wget --no-check-certificate --content-disposition -q -O /app.jar https://github.com/alibaba/Sentinel/releases/download/1.8.1/sentinel-dashboard-1.8.1.jar
#健康检查 -s 静默模式，不下载文件
#HEALTHCHECK CMD wget -s http://127.0.0.1:14030/actuator/health || exit 1
#8718控制台端口，8719为数据采集端口，他需要从被采集服务的8719进行收集数据
CMD ["java","-Dserver.port=8718","-Dcsp.sentinel.dashboard.server=localhost:8718","-Dproject.name=sentinel-dashboard","-Dcsp.sentinel.api.port=8719","-jar","app.jar"]
```

#### 部署

```yaml
 #部署注意需要和其他服务部署到一个stack里面，不然8719是访问不了的
  sentinel:
    restart: always  
    image: exxk/sentinel:1.8.1
    ports:
      - "8718:8718"
```

访问通过127.0.0.1:8718进行控制台的访问，默认用户名密码是sentinel/sentinel

