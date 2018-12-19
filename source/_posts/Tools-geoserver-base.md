---
title: Tools-geoserver-base
date: 2018-08-17 11:00:14
updated: 2018-12-12 10:47:58
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

# FWTools 切图

### tif切图

1. 下载[FWTools-linux-2.0.6.tar.gz](http://fwtools.loskot.net/FWTools-linux-2.0.6.tar.gz),复制文件到`cp FWTools-linux-2.0.6.tar.gz ~/`,然后解压文件`tar -zxvf FWTools-linux-2.0.6.tar.gz`
2. 使用wsl沙河系统安装，执行`sudo apt update`然后安装`sudo apt install python`安装默认的2.x版本
3. 修改安装脚本`vim install.sh`修改最后一行`/bin/python`为`/usr/bin/python`
4. 安装`sudo apt install python-gdal`插件
5. 测试，执行`gdal_retile.py -v -r bilinear -levels 10 -ps 256 256 -co "TILED=YES" -co COMPRESS=LZW -targetDir /mnt/c/Users/xuan/Desktop/tse/ /mnt/c/Users/xuan/Desktop/kongjiang.tif`

### shp转mysql

1. 安装`sudo apt install gdal-bin`
2. 执行`ogr2ogr -f "GeoJSON" china.json 保护动物.shp`先把shp文件转为json，检查json文件编码是否为utf-8
3. 再把json导入数据库`ogr2ogr -f "MySQL" MySQL:"yglgeoserver,user=root,host=192.168.1.230,password=lfadmin" -lco engine=INNODB china.json`，不直接将shp导入数据库是因为编码问题，导致导入报错

### 编写批量导入数据shell脚本

```bash
#! /bin/bash
for FILE in *.shp
do
        echo "printf file: $FILE..."
        #${FILE%.*}.json为新的名字，例如文件名（$FILE）为 ss.shp 那么新的名字（${FILE%.*}.json）为ss.json
        ogr2ogr -f "GeoJSON" "${FILE%.*}.json" "$FILE"
        #批量替换id为shpId字段，i为忽略大小写，见问题1
        sed -i 's/"Id"/"shpId"/i' "${FILE%.*}.json"
        ogr2ogr -f "MySQL" MySQL:"wzsgeoserver,user=root,host=192.168.1.230,password=lfadmin" -lco engine=INNODB "${FILE%.*}.json"

done
exit
```

#### 问题

1. 批量转换时提示`Warning 1: Feature id not preserved`

   **原因**:是因为json数据中含有id，且id字段的值重复，导致识别为相同数据例如

   ```json
   {
   "type": "FeatureCollection",
   "name": "橡胶天然林样地",
   "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
   "features": [
   { "type": "Feature", "properties": { "Id": 0, "坐标点": "aa", "编号": null, "树种": null, "胸径": null, "树高": null, "东西": null, "南北": null, "序号": 3, "X坐标": 109.33121961000001, "Y坐标": 18.9831775639 }, "geometry": { "type": "Point", "coordinates": [ 107.331219609524425, 18.973177563938192 ] } },
   { "type": "Feature", "properties": { "Id": 0, "坐标点": "ab", "编号": null, "树种": null, "胸径": null, "树高": null, "东西": null, "南北": null, "序号": 3, "X坐标": 109.331143725, "Y坐标": 18.983130045799999 }, "geometry": { "type": "Point", "coordinates": [ 109.331143724995911, 18.973130045772864 ] } }
   ]}
   ```

   **解决**:用文本工具批量删除或替换掉id字段，会自动生产id，如果有这字段就不会自动生成

### she 转 kml

```bash
ogr2ogr -f KML output.kml input.shp 
```



### geoserver

[所有版本](https://build.geoserver.org/geoserver/)

[idea运行](https://docs.geoserver.org/latest/en/developer/quickstart/intellij.html) 从[github](https://github.com/geoserver/geoserver)的src目录



https://github.com/NASAWorldWind/WorldWindJava

geoserver 安装[dds/bls](https://docs.geoserver.org/stable/en/user/community/dds/index.html)扩展



高层数据https://www.jianshu.com/p/d68fffeb8e33未实验