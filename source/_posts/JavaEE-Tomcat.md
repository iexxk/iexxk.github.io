---
title: JavaEE-Tomcat
date: 2018-05-02 16:48:44
updated: 2018-05-02 17:00:03
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

