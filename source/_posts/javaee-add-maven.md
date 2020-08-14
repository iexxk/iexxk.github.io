---
title: JavaEE-add-maven
date: 2019-02-13 15:28:13
updated: 2019-02-17 22:11:37
categories: JavaEE
tags: [maven]
---

### java项目添加maven框架

1. `右键项目->Add Frameworks Support->[✔]maven`会自动整理项目结构

2. 修改`pom.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
       <modelVersion>4.0.0</modelVersion>
   
       <groupId>com.surelive.api</groupId>
       <artifactId>ApiServer</artifactId>
       <version>1.0-SNAPSHOT</version>
       <!--设置打包格式-->
       <packaging>war</packaging>
   
       <properties>
           <!--设置File encoding,没设置默认GBK会提示错误-->
           <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
           <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
           <!--设置java编译版本-->
           <maven.compiler.source>1.7</maven.compiler.source>
           <maven.compiler.target>1.7</maven.compiler.target>
           <maven.compiler.compilerVersion>1.7</maven.compiler.compilerVersion>
       </properties>
       
       <!-- 配置maven地址 -->
       <distributionManagement>
           <repository>
               <!--这里的id要和maven里的的settings.xml的id一致-->
               <id>nexus-releases</id>
               <name>Nexus Release Repository</name>
               <url>http://112.74.51.136:14002/repository/maven-releases/</url>
           </repository>
           <snapshotRepository>
               <id>nexus-snapshots</id>
               <name>Nexus Snapshot Repository</name>
               <url>http://112.74.51.136:14002/repository/maven-snapshots/</url>
           </snapshotRepository>
       </distributionManagement>
       
   </project>
   ```

3. 添加maven解决依赖,可以解压jar查看具体版本（有的没有，可以上传到nexus仓库）

   注意：编译不报错，不代表maven依赖正确

4. 在`APP\src\main\webapp\WEB-INF\web.xml`添加`web.xml`,里面有启动顺序

5. 移动配置文件conf复制到`APP\src\main\resources`

6. 代码如果采用绝对路径引用配置文件，去掉`CONFIG_PATH = "/mybatis-config.xml";`里面的`/`会读取默认的`APP\src\main\resources`目录下的配置文件

   注意：win10下注意tomcat的路径不能含空格等特殊符号，例如`Program Files`等，错误显示为某某文件找不到

### 常见问题

1. 现象

   ```powershell
   [WARNING] Using platform encoding (GBK actually) to copy filtered resources, i.e. build is platform dependent!
   [ERROR] /D:/xuan/workspace/ApiServer/src/main/java/com/xx/api/server/timer/BaseTimerTask.java:[25,77] 编码GBK的不 可映射字符
   ```

   解决：在pom.xml添加

   ```xml
   <project ...> 
       <properties>
           <!--设置File encoding,没设置默认GBK会提示错误-->
           <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
           <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
       </properties>
   </project>
   ```

2. `[ERROR] /.../SysData.java:[12,81] -source 1.5 中不支持 diamond 运算符
   (请使用 -source 7 或更高版本以启用 diamond 运算符)`

   解决：在pom.xml添加

   ```xml
   <project ...> 
       <properties>
           <!--设置java编译版本-->
           <maven.compiler.source>1.7</maven.compiler.source>
           <maven.compiler.target>1.7</maven.compiler.target>
           <maven.compiler.compilerVersion>1.7</maven.compiler.compilerVersion>
        </properties>
   </project>      
   ```

3. `NoClassDefFoundError: redis/clients/jedis/JedisCommands`

   分析：编译打包时并没有任何错误，因为其他包里面有jedis的这个子包，所以编译通过了，但是运行时却找不到相应的版本所以导致该错

   解决：添加相应的`jedis`依赖

4. `SchedulerException: SchedulerPlugin class 'org.quartz.plugins.xml.XMLSchedulingDataProcessorPlugin' could not be instantiated.`

   分析：因为使用声明式的不能直接分析出依赖问题

   解决：找到`XMLSchedulingDataProcessorPlugin`该class，复制该类的所有`import`到项目里面的一个随便的java文件，查看是否找不到包（有红线），然后添加缺的包的依赖



### 知识点

`NoClassDefFoundError`  一般是指没有jar

[ClassNotFoundException和NoClassDefFoundError的区别](https://my.oschina.net/jasonultimate/blog/166932)

