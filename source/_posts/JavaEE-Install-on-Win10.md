---
title: win10下JavaEE之环境搭建
date: 2017-03-15 10:20:28
updated: 2018-04-25 20:47:32categories: JavaEE
tags: [JavaEE,环境搭建,基础]
---

#### MySQL安装

1. 下载[MySQL Community Server 5.7.17](https://dev.mysql.com/downloads/mysql/)文件名

2. 安装目录[C:\Develop\mysql-5.7.17-winx64](C:\Develop\mysql-5.7.17-winx64)

3. 设置工作目录复制`my-default.ini`重命名为`my.ini`修改里面

   ```ini
    # These are commonly set, remove the # and set as required.
    basedir = "C:\Develop\mysql-5.7.17-winx64"
    datadir = "E:\DevelopmentWorkspace\mysql-5.7.17-workspase"
   ```

   ###### 注：其中 basedir=你的mysql目录，datadir=数据存放目录

4. 以**管理员**身份运行cmd,切换到`C:\Develop\mysql-5.7.17-winx64\bin`执行`mysqld -install`

5. 执行`mysqld --initialize` 如果执行错误，删除数据存放目录，重新执行

6. 运行mysql执行`net start mysql`

7. 停止mysql执行`net stop mysql`

   ​

#### Tomcat 安装

1. 下载[apache-tomcat-8.5.12-windows-x64](http://tomcat.apache.org/download-80.cgi)
2. 安装目录[C:\Develop\apache-tomcat-8.5.12](C:\Develop\apache-tomcat-8.5.12)

#### idea 安装

1. 下载[ideaIU-2016.3.5.exe](https://www.jetbrains.com/idea/)
2. 安装目录[C:\Develop\IntelliJ IDEA 2016.3.5](C:\Develop\IntelliJ IDEA 2016.3.5)
3. 智能提示忽略大小写`Editor->General->Code Completion:{Casesensitive completion:None}`
4. 取消自动打开上次的项目`Appearance->System Settings:{Reopen last project on startup:false}`

###### 美化

1. 安装`Material Theme UI插件` 
2. 下载主题样式[http://color-themes.com](http://color-themes.com/?view=index)
3. 导入主题Ladies Night 2: `File->Import Settings...`

#### eclipse 安装

1.下载[https://eclipse.org/](https://eclipse.org/)

