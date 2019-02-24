---
title: JavaEE-Tomcat
date: 2018-05-02 16:48:44
updated: 2019-02-20 18:00:57
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



