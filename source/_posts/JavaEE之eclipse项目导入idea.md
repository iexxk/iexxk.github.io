---
title: eclipse项目导入idea
date: 2017-04-20 20:57:28
categories: JavaEE
tags: [JavaEE,idea,项目移植]
---

###  Project Structure设置

##### Modules 设置

###### Sources

```
—— e:\workspace\test    //工程目录
—— ——.idea
—— ——.settings
—— ——.build
—— —— ——.classes
—— ——META-INF
—— ——out                 //默认输出目录(设置为Excluded)
—— —— ——artifacts
—— —— —— ——test           //编译好的webapp
—— —— ——production
—— ——src             //java代码目录(设置为Sources)
—— ——WebContent   //web静态代码目录(含js、jsp、html、css...)
```

###### Paths

编译输出目录选择默认选项Inherit project....path

###### Dependencies

添加工程需要jar包，一般在`/WebContent/WEB-INF/lib`，必须添加tomcat的library,不然servlet着不到包

##### Facets 设置

添加***Web***选择自己的项目

* 更改Deployment Descriptors为自己项目的web.xml路径（`/WebContent/WEB-INF/web.xml`）
* 更改Web Resource Directories为自己项目的web资源目录(`.../WebContent`)  path ... root 设置为`/`根目录
* Source Roots勾选.../src路径

##### Artifacts

设置webapp发布部署输出目录

 添加`Web Application:Exploded`

output directory: `c:\develop\tomcat\webapp\test`

```
——output root    //这个是output directory设置的目录
—— ——WEB-INF
—— —— ——classes
—— —— —— ——'test' compile output   //项目Java编译src中java输出class的目录
—— —— ——lib              //jar包目录
—— ——'test' module:'web' facet resources //设置facet resources 为自己的web目录（/WebContent）
//Available Elements(右边)是提示，可以双击直接在右边生成建议目录，设置了test下没有二级目录
```

### 配置运行tomcat Server

##### Run/Debug Configurations设置

###### Server 默认

###### Deployment   

* 点击+，添加要运行的test项目
* application context 设置为`/test`

访问地址[localhost:8080/test](localhost:8080/test)或[127.0.0.1:8080/test](127.0.0.1:8080/test)

[eclipse java web项目导入到idea](http://jingyan.baidu.com/article/ca41422f2145641eae99edb9.html)