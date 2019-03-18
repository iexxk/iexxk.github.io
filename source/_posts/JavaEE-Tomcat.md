---
title: JavaEE-Tomcat
date: 2018-05-02 16:48:44
updated: 2019-03-09 14:20:58
categories: JavaEE
tags: [Tomcat,JavaEE]
---

#### 安装运行

1. tomcat 下载[apache-tomcat-8.5.12-windows-x64](http://tomcat.apache.org/download-80.cgi)然后解压安装

2. 编辑`tomcat/conf/server.xml`

   ```xml
   <!-- 9301为自定义端口号,默认为8080 -->  
   <Connector port="9301" protocol="HTTP/1.1"
                  connectionTimeout="20000"
                  redirectPort="8443" />
   <!--复制或者修改host-->
   <Host name="localhost"  appBase="webapps"
         unpackWARs="true" autoDeploy="true">
      <!-- 新加context  /app为url上下文,app为webapps下的app.war包-->	
     <Context path="/app" docBase="app" reloadable="false" 
              source="org.eclipse.jst.jee.server:tsj-spring"/>
     <Valve className="org.apache.catalina.valves.AccessLogValve" 
            directory="logs" prefix="localhost_access_log" suffix=".txt" 
            pattern="%h %l %u %t &quot;%r&quot; %s %b" />
   </Host>
   ```

3. 运行tomcat,window下双击打开bin目录下的`startup.bat`启动app.war

4. 访问为`ip:9301/app/`

## tomcat远程自动部署

1. 安装[tomcat8.5.x](https://tomcat.apache.org/download-80.cgi)

2. 修改tomcat配置文件`conf/server.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <Server port="8019" shutdown="SHUTDOWN">
     <Listener className="org.apache.catalina.startup.VersionLoggerListener" />
     <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
     <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
     <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
     <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />
     <GlobalNamingResources>
       <Resource name="UserDatabase" auth="Container"
                 type="org.apache.catalina.UserDatabase"
                 description="User database that can be updated and saved"
                 factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                 pathname="conf/tomcat-users.xml" />
     </GlobalNamingResources>
     <Service name="Catalina">
       <Connector port="8005" protocol="HTTP/1.1"
                  connectionTimeout="20010"
                  redirectPort="8454" />
       <Connector port="8021" protocol="AJP/1.3" redirectPort="8454" />
   
       <Engine name="Catalina" defaultHost="H8005">
   
         <Realm className="org.apache.catalina.realm.LockOutRealm">
           <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
                  resourceName="UserDatabase"/>
         </Realm>
   
         <Host name="H8005"  appBase="webapps"
               unpackWARs="true" autoDeploy="true">
   
           <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                  prefix="localhost_access_log" suffix=".txt"
                  pattern="%h %l %u %t &quot;%r&quot; %s %b" />
   
         </Host>
       </Engine>
     </Service>
   </Server>
   ```

3. 修改`conf/tomcat-users.xml`

   ```xml
   <tomcat-users xmlns="http://tomcat.apache.org/xml"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
                 version="1.0">
                 
   <role rolename="admin-gui"/>
   <role rolename="admin-script"/>
   <role rolename="manager-gui"/>
   <role rolename="manager-script"/>
   <role rolename="manager-jmx"/>
   <role rolename="manager-status"/>
   <user username="admin" password="ideaadmin" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-script,admin-gui"/>
   
   </tomcat-users>
   ```

4. 启动tomcat执行`./bin/catalina.sh start | tail -f ./logs/catalina.out`,如果要修改启动内存，启动前提前修改`catalina.sh`

5. 在`conf/Catalina/h8005`添加`manager.xml`

   ```xml
   <Context privileged="true" antiResourceLocking="false"
            docBase="${catalina.home}/webapps/manager">
       <Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="^.*$" />
   </Context>
   ```

6. 然后打开http://ip:8005/manager,输入用户名`admin`密码`idaeadmin`,进入之后保留**manager**删除其他所有applications

7. 修改maven的`.m2/setting.xml`文件

   ```xml
     <servers>
       <server>
         <id>innerCs</id>
         <username>admin</username>
         <password>ideaadmin</password>
       </server>
         ...
     </servers>    
   ```

8. 在项目里面的`pom.xml`添加

   ```xml
      <build>
           <finalName>InnerCS</finalName>
           <plugins>
   			...
               <plugin>
                   <groupId>org.apache.tomcat.maven</groupId>
                   <artifactId>tomcat7-maven-plugin</artifactId>
                   <version>2.2</version>
                   <configuration>
                       <url>http://ip:8005/manager/text</url>
                       <path>/</path>
                       <uriEncoding>UTF-8</uriEncoding>
                       <server>innerCs</server>
                   </configuration>
               </plugin>
           </plugins>
       </build>
   ```

9. 编译`Lifecyle->clean->install`部署`lifecyle->deploy`发布到maven私库

10. 远程第一次部署`plugins->tomcat7->deploy`，会上传`ROOT.war`到`/webapps/`并解压运行生成`ROOT`因为我配置的path为`/`所以是ROOT

###### 注意事项

1. 第九步时，如果时maven多模块项目，需要在父项目，添加上传依赖jar的地址

   ```xml
   <!-- 配置maven地址 -->
   <distributionManagement>
       <snapshotRepository>
           <id>nexus-snapshots</id>
           <name>Nexus Snapshot Repository</name>
           <url>http://192.168.101.200:8081/repository/maven-snapshots/</url>
       </snapshotRepository>
   </distributionManagement>
   ```

2. 还需要在maven的`setting.xml`配置maven的用户名，才有权限上传

   ```xml
   	<server>
         <id>nexus-snapshots</id>
         <username>admin</username>
         <password>admin123</password>
       </server>
   ```

3. 多模块项目需要在父级里面进行`clean-install-deploy`,注意勾选idea maven右侧菜单里面的`Profiles`，不然父级不知道编译那个子项目



### 常见问题

1. tomcat启动时出现`java.lang.IllegalArgumentException: Illegal character(s) in message header field: Pragma:`

   ```
   java.lang.IllegalArgumentException: Illegal character(s) in message header field: Pragma:
   2019-02-20 17:40:47 331 - 	at sun.net.www.protocol.http.HttpURLConnection.checkMessageHeader(HttpURLConnection.java:511)
   2019-02-20 17:40:47 331 - 	at sun.net.www.protocol.http.HttpURLConnection.isExternalMessageHeaderAllowed(HttpURLConnection.java:481)
   2019-02-20 17:40:47 331 - 	at sun.net.www.protocol.http.HttpURLConnection.setRequestProperty(HttpURLConnection.java:2895)
   2019-02-20 17:40:47 331 - 	at sun.net.www.protocol.https.HttpsURLConnectionImpl.setRequestProperty(HttpsURLConnectionImpl.java:325)
   2019-02-20 17:40:47 331 - 	at mmo.common.utils.HttpUtils.sendPost(HttpUtils.java:28)
   2019-02-20 17:40:47 331 - 	at com.surelive.app.server.service.QQGroupApiService$1.run(QQGroupApiService.java:169)
   2019-02-20 17:40:47 331 - 	at com.surelive.app.server.entities.ext.QueueThreadHandle.run(QueueThreadHandle.java:52)
   2019-02-20 17:40:47 331 - 	at com.surelive.app.server.service.QueueThreadPoolServer$1.run(QueueThreadPoolServer.java:26)
   2019-02-20 17:40:47 331 - 	at java.lang.Thread.run(Thread.java:748)
   ```

   解决：执行`env`检查环境变量中是否有`JAVA_HOME`,没有设置好这些环境变量



