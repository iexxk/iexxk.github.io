---
title: springboot打包套壳
date: 2020-08-24 11:13:54
updated: 2020-08-25 11:48:04
categories: spring
tags: [spring,maven]
---

## 需求

客户需要git自动化部署，但是又不能提供源码，所以打包成jar包，然后在套壳，依赖jar进行部署

## 原理

```mermaid
graph LR
A(springboot源项目)-->G(打包发布成jar,含main class)--做为依赖-->L[springboot套壳项目]-->E[自动部署]
```

## 利用maven仓库打包步骤

1. 删除源项目`pom.xml`里面的`<build></build>`标签及里面的内容

2. 如果项目里面有公共项目本地依赖(common等)，都要上传，因为打包jar不会打包依赖到jar包里面，上传需要在`pom.xml`里面添加，然后执行mave lifecycle  里面的 deploy

   ```xml
   	<distributionManagement>
   		<repository>
   			<!--这里的id要和maven里的的settings.xml的id一致-->
   			<id>nexus</id>
   			<name>Nexus Release Repository</name>
   			<url>http://ipaddress/repository/maven-third/</url>
   		</repository>
   	</distributionManagement>
   ```

   注意:

   1. 上传报错的话，检查依赖包是否设置`<version>0.0.1-SNAPSHOT</version>`需要改成`<version>0.0.1</version>`因为`SNAPSHOT`上传需要特殊权限

   2. 上传没有权限，需要添加nexus中仓库的角色权限`nx-repository-view-*-*-edit`

   3. 检查maven的设置文件`setting.xml`

      ```xml
      <servers>
          <server>
              <id>nexus</id>
              <username>read</username>
              <password>read***</password>
          </server>
      </servers>
      ```

   4. 如果是多项目结构，外面的父项目框架，不需要deploy，在`pom.xml`添加下面这个设置

      ```xml
          <properties>
              <maven.deploy.skip>true</maven.deploy.skip>
          </properties>
      ```

3. 新建个maven空项目，其中pom.xml如下

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
       <modelVersion>4.0.0</modelVersion>
   
    <!-- 这个千万不能添加，添加会提示找不到main class-->
   <!--	<parent>-->
   <!--		<groupId>org.springframework.boot</groupId>-->
   <!--		<artifactId>spring-boot-starter-parent</artifactId>-->
   <!--		<version>2.1.12.RELEASE</version>-->
   <!--	</parent>-->
     
       <groupId>com.zy</groupId>
      <!-- id不能和原项目一样，不然会提示自己依赖自己-->
       <artifactId>bpf_pf_router_zy</artifactId>
       <version>1.0.0</version>
       <packaging>jar</packaging>
       <name>bpf_pf_router_zy</name>
   
       <properties>
           <java.version>1.8</java.version>
           <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
           <skipTests>true</skipTests>
       </properties>
   
       <dependencies>
          <!-- 源项目打包成的jar-->
       	<dependency>  
       		<groupId>com.nantian</groupId>  
       		<artifactId>bpf_pf_router</artifactId>  
       		<version>1.0.0</version>  
   		</dependency>  
       </dependencies>
     
   		<!-- 添加主类，主类在原项目，也就是第一步里面删除的那部分里面有-->
       <build>
           <plugins>
               <plugin>
                   <groupId>org.springframework.boot</groupId>
                   <artifactId>spring-boot-maven-plugin</artifactId>
                   <executions>
   					<execution>
   						<goals>
   							<goal>repackage</goal>
   						</goals>
   						<configuration>
   							<mainClass>com.nantian.bpf.router.App</mainClass>
   						</configuration>
   					</execution>
   				</executions>
               </plugin>
           </plugins>
       </build>
   </project>
   ```

## 利用maven-dependency-plugin进行本地打包

1. 在壳项目pom.xml添加如下配置

   ```xml
       .......
       <repositories>
           <repository>
               <id>lib</id>
               <url>file:${project.basedir}/lib</url>
           </repository>
       </repositories>
       <build>
               ........
               <plugin>
                   <artifactId>maven-dependency-plugin</artifactId>
                   <executions>
                       <execution>
                           <phase>compile</phase>
                           <goals>
                               <goal>copy-dependencies</goal>
                           </goals>
                           <configuration>
                               <outputDirectory>${project.build.directory}/lib</outputDirectory>
                           </configuration>
                       </execution>
                   </executions>
               </plugin>
           </plugins>
       </build>
       ......
   ```

2. 把maven本地库里面的原项目的依赖放到壳项目的lib目录里面

   ```properties
   ├── README.md
   ├── lib
   │   └── com
   │       └── nantian
   │           └── bpf_pf_router
   │               ├── 1.0.0
   │               │   ├── _remote.repositories
   │               │   ├── bpf_pf_router-1.0.0.jar
   │               │   └── bpf_pf_router-1.0.0.pom
   │               ├── maven-metadata-local.xml
   │               ├── maven-metadata-nexus.xml
   │               └── resolver-status.properties
   ├── pom.xml
   ├── src
   │   └── main
   │       ├── java
   │       └── resources
   │           └── bootstrap.properties
   └── target
       └── cnpc_dj_business_facerouter-1.0.0.jar
   ```

3. 更新时将jar更新到lib目录时，如果只更新了jar，需要注意清除maven本地库(lib 加载到 maven本地库，本地库在打包进jar)，否则就更新lib里面的其他文件，这样就能识别出来lib发生了更新

   ```mermaid
   graph LR
   a[lib]-->b[maven本地库]-->c[jar]
   ```

## 利用lib打包步骤(废弃暂时不能解决)

1. 改造壳项目pom.xml,修改依赖为本地依赖

   ```xml
       <dependencies>
       	<dependency>  
       		<groupId>com.nantian</groupId>  
       		<artifactId>bpf_pf_router</artifactId>  
       		<version>1.0.0</version>
               <scope>system</scope>
               <systemPath>${project.basedir}/src/libs/bpf_pf_router-1.0.0.jar</systemPath>
   		</dependency>
       </dependencies>
   ```

2. 把原项目jar包放到项目src目录

3. 改造壳项目pom.xml,修改打包参数，不修改，不会把lib打包进jar包

   ```xml
   <plugin>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-maven-plugin</artifactId>
       <configuration>
        <!--添加下面这句 -->   
       <includeSystemScope>true</includeSystemScope>
       </configuration>
   </plugin>     
   ```

#### 问题

1. jar包里面包含依赖，利用本地jar包打包时，依赖不自动打入(暂时未能解决)



