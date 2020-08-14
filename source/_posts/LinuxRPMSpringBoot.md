---
title: Linux-RPM-springBoot
date: 2019-05-24 16:03:14
updated: 2019-06-13 10:21:26
categories: Linux
tags: [RPM]
---

## rpm打包SpringBoot实战

1. 环境需求安装rpm

   ```bash
   #centos
   yum -y install rpmdevtools
   #mac
   brew install rpm
   ```

2. 添加插件

   ```xml
     <properties>
   			.......
   	  <rpm.release>0.3.0</rpm.release>
   	  <rpm.install.path>/home/face/java</rpm.install.path>
   	  <rpm.prefix>/data/micro-services/9090-web-api-jar</rpm.prefix>
     </properties>	
   
   <build>
   	    <finalName>${autoPackage.name}</finalName>
   		<plugins>	
   				<plugin>
   				<groupId>org.codehaus.mojo</groupId>
   				<artifactId>rpm-maven-plugin</artifactId>
   				<version>2.2.0</version>
   				<extensions>true</extensions>
   				<executions>
   					<execution>
   						<goals>
   							<goal>rpm</goal>
   						</goals>
   					</execution>
   				</executions>
   				<configuration>
   					<prefix>${rpm.prefix}</prefix>
   					<distribution>myron</distribution>
   					<group>myron.com</group>
   					<packager>hello</packager>
   					<version>${project.version}</version>
   					<autoRequires>true</autoRequires>
   					<release>3</release>
   					<requires>
   						<require>java-1.7.0 >= 1.7</require>
   					</requires>
   					<mappings>
   						<mapping>
   							<!-- 安装rpm后指向的服务器安装目录  -->
   							<directory>${rpm.install.path}/${project.artifactId}</directory>
   							<filemode>755</filemode>
   							<username>root</username>
   							<groupname>root</groupname>
   							<sources>
   								<source>
   									<location>target/${project.artifactId}.jar</location>
   								</source>
   							</sources>
   						</mapping>
   						<!-- 复制安装相关脚本命令 根据具体项目需要决定是否使用-->
   <!--						<mapping>-->
   <!--							<directory>${rpm.install.path}/${project.artifactId}/bin</directory>-->
   <!--							<filemode>750</filemode>-->
   <!--							<username>root</username>-->
   <!--							<groupname>root</groupname>-->
   <!--							<sources>-->
   <!--								<source>-->
   <!--									<location>src/bin</location>-->
   <!--								</source>-->
   <!--							</sources>-->
   <!--						</mapping>-->
   
   						<!--配置软连接注册服务起停项目,相当于:ln -sf myapp.jar /etc/init.d/myapp)
                               启动: systemctl start myapp
                               停止: systemctl stop myapp
                               重启: systemctl restart myapp
                               查看日志: journalctl -u myapp-->
   <!--						<mapping>-->
   <!--							<directory>/etc/init.d</directory>-->
   <!--							<filemode>750</filemode>-->
   <!--							<username>root</username>-->
   <!--							<groupname>root</groupname>-->
   <!--							<sources>-->
   <!--								<softlinkSource>-->
   <!--									<location>${rpm.install.path}/${project.artifactId}/${project.artifactId}-${project.version}.jar</location>-->
   <!--									<destination>${project.artifactId}</destination>-->
   <!--								</softlinkSource>-->
   <!--							</sources>-->
   <!--						</mapping>-->
   					</mappings>
   					<preinstallScriptlet>
   						<script>echo "installing ${project.name} now"</script>
   					</preinstallScriptlet>
   					<postinstallScriptlet>
   						<!-- 通过软链接 配置"service demo-swagger2 " 相关操作命令启动-->
   						<!-- 使用上面softlinkSource配置替代
                           <script>
                               rm -f /etc/init.d/${project.artifactId};
                               ln -sf ${rpm.install.path}/${project.artifactId}/bin/startup.sh /etc/init.d/demo-swagger2;
                           </script>
                           -->
   					</postinstallScriptlet>
   					<preremoveScriptlet>
   						<script>
   							<!--rm -f /etc/init.d/${project.artifactId};-->
   							echo "uninstalling ${project.name} success";
   						</script>
   						<!-- 引用脚本方式
                           <scriptFile>src/main/scripts/preremove</scriptFile>
                           <fileEncoding>utf-8</fileEncoding>
                           -->
   					</preremoveScriptlet>
   				</configuration>
   			</plugin>
         ........
   		</plugins>
   	</build>
   </project>
   ```



空配置

```xml
 <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>rpm-maven-plugin</artifactId>
                <version>2.2.0</version>
                <inherited>false</inherited>
                <executions>
                    <execution>
                        <!-- unbinds rpm creation from maven lifecycle -->
                        <phase>none</phase>
                        <goals>
                            <goal>attached-rpm</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <release>1</release>
                    <distribution>loganshen</distribution>
                    <group>ifengkou.github.io</group>
                    <packager>loganshen</packager>
                    <prefix>/opt/soft</prefix>
                    <mappings>
                        <mapping>
                            <directory>/tmp</directory>
                        </mapping>
                    </mappings>
                </configuration>
            </plugin>
```

`package rpm:rpm -U`





### 参考

[maven使用rpm-maven-plugin构建RPM包](https://blog.csdn.net/Myron_007/article/details/80899368)

