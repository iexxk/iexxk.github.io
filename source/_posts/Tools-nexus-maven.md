---
title: Tools-nexus-maven
date: 2018-09-06 08:42:44
updated: 2018-12-12 10:47:58
categories: 工具
tags: [nexus3,maven]
---

# maven私库nexus3搭建使用

### [sonatype/nexus3](https://github.com/sonatype/docker-nexus3)安装

1. 创建挂载目录`mkdir -p v-nexus/data`并修改目录权限`chown -R 200 v-nexus/data`

2. 创建部署脚本

   ```yaml
   # 默认用户名admin/admin123
   version: '3.2'
   
   services:
     nexus:
       restart: always
       image: sonatype/nexus3
       ports:  #自定义端口
         - target: 8081
           published: 18081   #只有worker能访问该端口
           protocol: tcp
           mode: host  #版本要求3.2
       volumes:
         - "/dockerdata/v-nexus/data:/nexus-data"
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == lfadmin]
   ```

3. 测试访问`http://192.168.1.213:18081/`然后输入admin和admin123进行登陆即可

### 配置yum代理

远程原remote url: http://maven.aliyun.com/nexus/content/groups/public

新建一个**type:yum(proxy)**

在新建一个组**yum(group)**,添加刚刚的代理地址,同理，可以添加elpe,docker等其他仓库代理

复制生成的地址http://192.168.1.230:18081/repository/yum-public/配置在`nexus.repo`

执行`vim /etc/yum.repos.d/nexus.repo`

```properties
[nexusrepo]
name=Nexus Repository
baseurl=http://192.168.1.230:18081/repository/yum-public/$releasever/os/$basearch/
enabled=1
gpgcheck=0
priority=1
```

`yum clean all`

`rm -rf  /etc/yum.repos.d/C*`

##### 注意

epel源需要单独配置，直接用public不识别

执行`vim /etc/yum.repos.d/nexus-epel.repo`

```properties
[nexus-epel-debuginfo]
name = Extra Packages for Enterprise Linux 7 - $basearch - Debug
baseurl = http://192.168.1.230:18081/repository/yum-epel/7/$basearch/debug
failovermethod = priority
enabled = 0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
gpgcheck = 0

[nexus-epel-source]
name = Extra Packages for Enterprise Linux 7 - $basearch - Source
baseurl = http://192.168.1.230:18081/repository/yum-epel/7/SRPMS
failovermethod = priority
enabled = 0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
gpgcheck = 0

[nexus-epel]
baseurl = http://192.168.1.230:18081/repository/yum-epel/7/$basearch
failovermethod = priority
gpgcheck = 0
name = EPEL YUM repo
```



### win10下[maven安装](https://maven.apache.org/download.cgi)

1. 下载[apache-maven-3.5.4-bin.zip](http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.zip)然后解压

2. 添加环境变量,新建系统环境变量`Maven_HOME`值为解压路径，编辑`path`环境变量添加`%Maven_HOME%\bin`

3. 命令窗口测试`mvn -v`，只支持cmd

4. 修改`apache-maven-3.5.4\conf\settings.xml`文件

   ```xml
   <!--jar本地缓存地址-->
   <localRepository>D:\MavenRepository</localRepository>
   ```

5. 完整的`setting.xml`设置

   ```XML
   <?xml version="1.0" encoding="UTF-8"?>
   
   <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
     
     <!--  jar本地缓存地址 -->
     <localRepository>D:\MavenRepository</localRepository>
   
     <pluginGroups>
   
     </pluginGroups>
   
     <proxies>
   
     </proxies>
   
   
     <servers>
   	 <!--配置权限,使用默认用户-->
       <server>
   	  <!--这里的id要和项目里的pom.xml的id一致-->
         <id>nexus-releases</id>
         <username>admin</username>
         <password>admin123</password>
       </server>
   	<server>
         <id>nexus-snapshots</id>
         <username>admin</username>
         <password>admin123</password>
       </server>
     </servers>
   
     <mirrors>
   
     </mirrors>
   
     <profiles>
       <profile>
         <id>MyNexus</id>
   
         <activation>
           <jdk>1.4</jdk>
         </activation>
   
         <repositories>
   	    <!-- 私有库地址-->
           <repository>
             <id>nexus</id>
             <name>>Nexus3 Repository</name>
   		   <!-- 注意修改成对应的IP,在nexus里面复制public里面的地址 -->
             <url>http://192.168.1.213:18081/repository/maven-public/</url>
         
   		  <releases> 
               <enabled>true</enabled> 
             </releases> 
             <!-- snapshots默认是关闭的，需要手动开启 --> 
             <snapshots> 
               <enabled>true</enabled> 
             </snapshots> 
           </repository>
   		
           </repositories>
   	          <pluginRepositories>
              <!--插件库地址-->
             <pluginRepository>
               <id>nexus</id>
               <url>http://192.168.1.213:18081/repository/maven-public/</url>
               <releases>
                 <enabled>true</enabled>
               </releases>
               <snapshots>
                 <enabled>true</enabled>
                </snapshots>
             </pluginRepository>
           </pluginRepositories>
       </profile>
   	
     </profiles>
   
    <!--激活profile-->
     <activeProfiles>
       <activeProfile>MyNexus</activeProfile>
     </activeProfiles>
   
   </settings>
   ```

6. 在项目的pom.xml修改或添加如下配置

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <project ...>
       ....
       <!-- 配置maven地址 -->
   	<distributionManagement>
   		<repository>
                <!--这里的id要和maven里的的settings.xml的id一致-->
   			<id>nexus-releases</id>
   			<name>Nexus Release Repository</name>
   			<url>http://192.168.1.213:18081/repository/maven-releases/</url>
   		</repository>
   		<snapshotRepository>
   			<id>nexus-snapshots</id>
   			<name>Nexus Snapshot Repository</name>
   			<url>http://192.168.1.213:18081/repository/maven-snapshots/</url>
   		</snapshotRepository>
   	</distributionManagement>
       ...
   </project>
   ```

7. 编译在cmd执行`mvn install`发布上传jar执行`mvn deploy`，可以到nexus地址进行检查

8. 使用私库下载和上传是一样的

### nexus3 配置阿里云代理仓库

1. 点击`Create Repository->maven2(proxy)`
2. 添加名字`aliyun-proxy`设置阿里云url地址`http://maven.aliyun.com/nexus/content/groups/public`
3. 设置阿里云优先级，在`maven-public`里面的group把刚刚创建的添加过去并移到maven-central上面
4. 设置允许发布release,在`maven-release`的hosted里面选择`allow redeploy`

### 发布上传jar包到nexus

语法：

```bash
mvn deploy:deploy-file \ 
  -DgroupId=<group-id> \
  -DartifactId=<artifact-id> \
  -Dversion=<version> \
  -Dpackaging=<type-of-packaging> \
  -Dfile=<path-to-file> \
  -DrepositoryId=<这里的id要和maven里的的settings.xml的id一致> \
  -Durl=<url-of-the-repository-to-deploy>
```

实战

```
mvn deploy:deploy-file \
-Dfile=spring-boot-starter-druid-0.0.1-SNAPSHOT.jar \
-DgroupId=cn.binux \
-DartifactId=spring-boot-starter-druid \ 
-Dversion=0.0.1-SNAPSHOT \ 
-Dpackaging=jar \ 
-DpomFile=spring-boot-starter-druid-0.0.1-SNAPSHOT.pom \
-DrepositoryId=nexus-snapshots \
-Durl=http://192.168.1.213:18081/repository/maven-snapshots/
```

上传jar包到私有maven仓库

```bash
mvn deploy:deploy-file -Dfile=spring-boot-starter-druid-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-druid -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar -DpomFile=spring-boot-starter-druid-0.0.1-SNAPSHOT.pom -DrepositoryId=nexus-snapshots -Durl=http://192.168.1.213:18081/repository/maven-snapshots/

mvn deploy:deploy-file -Dfile=spring-boot-starter-dubbox-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-dubbox -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar -DpomFile=spring-boot-starter-dubbox-0.0.1-SNAPSHOT.pom -DrepositoryId=nexus-snapshots -Durl=http://192.168.1.213:18081/repository/maven-snapshots/

mvn deploy:deploy-file -Dfile=spring-boot-starter-redis-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-redis -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar -DpomFile=spring-boot-starter-redis-0.0.1-SNAPSHOT.pom -DrepositoryId=nexus-snapshots -Durl=http://192.168.1.213:18081/repository/maven-snapshots/

#这个不是snapshots要发布到releases，注意设置nexus为允许发布，看jar报后缀，没有`SNAPSHOT`就是release
mvn deploy:deploy-file -Dfile=dubbo-2.8.4.jar -DgroupId=com.alibaba -DartifactId=dubbo -Dversion=2.8.4 -Dpackaging=jar -DrepositoryId=nexus-releases -Durl=http://192.168.1.213:18081/repository/maven-releases/

mvn deploy:deploy-file -Dfile=fastdfs-1.24.jar -DgroupId=org.csource -DartifactId=fastdfs -Dversion=1.24 -Dpackaging=jar -DrepositoryId=nexus-releases -Durl=http://192.168.1.213:18081/repository/maven-releases/

mvn deploy:deploy-file -Dfile=examples-1.0.jar -DgroupId=com.haikang -DartifactId=examples -Dversion=1.0 -Dpackaging=jar -DrepositoryId=nexus-releases -Durl=http://192.168.1.230:18081/repository/maven-releases/
```

本地安装jar包到本地maven仓库

```bash
mvn install:install-file -Dfile=spring-boot-starter-druid-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-druid -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar
mvn install:install-file -Dfile=spring-boot-starter-dubbox-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-dubbox -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar
mvn install:install-file -Dfile=spring-boot-starter-redis-0.0.1-SNAPSHOT.jar -DgroupId=cn.binux -DartifactId=spring-boot-starter-redis -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar
mvn install:install-file -Dfile=dubbo-2.8.4.jar -DgroupId=com.alibaba -DartifactId=dubbo -Dversion=2.8.4 -Dpackaging=jar
mvn install:install-file -Dfile=fastdfs-1.24.jar -DgroupId=org.csource -DartifactId=fastdfs -Dversion=1.24 -Dpackaging=jar
```

### 问题

1. 下载了找不到包，解决，删除项目重新导入，重新maven依赖
2. 刚上传或添加了新的jar到私库，无法下载，解决，删除本地仓库的该包目录