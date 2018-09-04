---
title: Tools-geoserver-base
date: 2018-08-17 11:00:14
updated: 2018-09-04 15:13:03
categories: 工具
tags: [geoserver]
---

## 安装

镜像地址：[kartoza/geoserver:latest](https://github.com/kartoza/docker-geoserver)

环境要求：最小内存4g

`docker-compose.yml`

```yaml
version: '3'

services:
  geoserver:
    restart: always
    image: 	kartoza/geoserver:latest	
    ports:
      - "14018:8080"
    volumes:
      - "/dockerdata/v-geoserver/data:/opt/geoserver/data_dir"
    environment:
      - JAVA_OPTS= '-Xmx3072m' 
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.hostname == worker]
```

### 使用

1. 登陆

   访问http://192.168.204.182:14018/geoserver/web/使用[admin](geoserver)登陆

2. 创建工作区

   命名：xuan(自定义)

   命名空间URI：http://geoserver.org/xuan

   - [x] 默认工作区

3. 新建数据存储

   选`栅格数据源->ImagePyramid` 

   复制图层数据（该数据可以用Fwtools切图）到挂载目录`/dockerdata/v-geoserver/data`

   点击浏览找到数据目录，然后保存

4. 发布图层

   保存成功后，点击发布按钮

   默认设置，保存

5. 测试预览图层

   点击`Layer Preview` 选择图层进行预览

### 字体安装

1. 查看支持的中文字体命令`fc-list :lang=zh`
2. 命令没有找到需要安装字体管理器`yum -y install fontconfig`
3. 字体目录`/usr/share/fontconfig`和`/usr/share/fonts`
4. 将window下或者下载字体文件ttc、ttf文件复制到fonts目录



## 问题

1. geoserver添加图层预览时提示`java.lang.OutOfMemoryError: GC overhead limit exceeded`该错误

   解决把`-Xmx`设置更大，如果是虚拟机最小内存必须设置4g

2. 跨域问题和添加插件

   ```dockerfile
   FROM kartoza/geoserver:latest
   #安装mysql插件
   ADD gt-jdbc-mysql-19.2.jar $CATALINA_HOME/webapps/geoserver/WEB-INF/lib/
   ADD mysql-connector-java-5.1.46.jar $CATALINA_HOME/webapps/geoserver/WEB-INF/lib/
   #解决跨域问题
   ADD web.xml $CATALINA_HOME/webapps/geoserver/WEB-INF/
   ADD java-property-utils-1.9.jar $CATALINA_HOME/webapps/geoserver/WEB-INF/lib/
   ADD cors-filter-1.7.jar $CATALINA_HOME/webapps/geoserver/WEB-INF/lib/
   #添加中文字体
   ADD chinese /usr/share/fonts/chinese/
   ```

   `web.xml`添加如下

   ```
   <filter>  
       <filter-name>CORS</filter-name>  
       <filter-class>com.thetransactioncompany.cors.CORSFilter</filter-class>  
       <init-param>  
        <param-name>cors.allowOrigin</param-name>  
           <param-value>*</param-value>  
       </init-param>  
       <init-param>  
        <param-name>cors.supportedMethods</param-name>  
           <param-value>GET, POST, HEAD, PUT, DELETE</param-value>  
       </init-param>  
       <init-param>  
        <param-name>cors.supportedHeaders</param-name>  
           <param-value>Accept, Origin, X-Requested-With, Content-Type, Last-Modified</param-value>  
       </init-param>  
       <init-param>  
           <param-name>cors.exposedHeaders</param-name>  
           <param-value>Set-Cookie</param-value>  
       </init-param>  
       <init-param>  
           <param-name>cors.supportsCredentials</param-name>  
           <param-value>true</param-value>  
       </init-param>  
   </filter>  
   <filter-mapping>  
       <filter-name>CORS</filter-name>  
       <url-pattern>/*</url-pattern>  
   </filter-mapping>
   
   ```

