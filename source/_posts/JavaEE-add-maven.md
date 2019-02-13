---
title: JavaEE-add-maven
date: 2019-02-13 15:28:13
updated: 2019-02-13 15:28:13
categories: JavaEE
tags: [maven]
---







java项目添加maven框架

1. `右键项目->Add Frameworks Support->[✔]maven`会自动整理项目结构

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

   