---
title: Java-protobuf
date: 2019-02-15 15:39:21
updated: 2019-02-28 18:16:35
categories: Java
tags: [Java,protobuf]
---

### protobuf介绍

就是一种

### protobuf简单测试

项目源码见[xuanfong1/springLeaning/protobuf](https://github.com/xuanfong1/springLeaning/tree/master/protobuf)

1. 在项目引入maven/gradle依赖`compile 'com.google.protobuf:protobuf-java:3.6.1'`

2. 下载[代码生成工具](https://github.com/protocolbuffers/protobuf/releases)，作用是将`file.proto`文件转换成其他语言（java/C++/GO/Python/C#/Dart）的文件,eg：这里选择window平台，版本和maven版本一致，因此选择[protoc-3.6.1-win32.zip](https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protoc-3.6.1-win32.zip),其他操作系统选择对应平台即可,然后解压，在bin目录可以看到`protoc.exe`文件，复制重命名`protoc-3.6.1-win32.exe`为了好区分版本，其他文件用不着

3. 编写一个测试`PersonMsg.proto`文件

   ```protobuf
   message Person {
   
       // ID（必需）
       required int32 id = 1;
   
       // 姓名（必需）
       required string name = 2;
   
       // email（可选）
       optional string email = 3;
   
       // 朋友（集合）
       repeated string friends = 4;
   }
   ```

4. 使用工具进行java代码生成，执行`.\protobuf\protoc-3.6.1-win32.exe --java_out=.\protobuf\src\main\java\com\exxk\protobuf\  .\protobuf\src\test\protobuf\PersonMsg.proto`

   注意，这里生成的代码`PersonMsg.java`里面是没有包名的，可以手动加入

5. 在`ProtobufApplicationTests.java`编写测试方法

   ```java
   import java.io.ByteArrayInputStream;
   import java.io.ByteArrayOutputStream;
   import java.io.IOException;
   import java.util.List;
   
   
   //@RunWith(SpringRunner.class)
   //@SpringBootTest
   public class ProtobufApplicationTests {
   
       @Test
       public void contextLoads() {
           // 按照定义的数据结构，创建一个Person
           PersonMsg.Person.Builder personBuilder = PersonMsg.Person.newBuilder();
           personBuilder.setId(1);
           personBuilder.setName("叉叉哥");
           personBuilder.setEmail("xxg@163.com");
           personBuilder.addFriends("Friend A");
           personBuilder.addFriends("Friend B");
           PersonMsg.Person xxg = personBuilder.build();
   
           // 将数据写到输出流，如网络输出流，这里就用ByteArrayOutputStream来代替
           ByteArrayOutputStream output = new ByteArrayOutputStream();
           try {
               xxg.writeTo(output);
           } catch (IOException e) {
               e.printStackTrace();
           }
   
           // -------------- 分割线：上面是发送方，将数据序列化后发送 ---------------
   
           byte[] byteArray = output.toByteArray();
   
           // -------------- 分割线：下面是接收方，将数据接收后反序列化 ---------------
   
           // 接收到流并读取，如网络输入流，这里用ByteArrayInputStream来代替
           ByteArrayInputStream input = new ByteArrayInputStream(byteArray);
   
           // 反序列化
           PersonMsg.Person xxg2 = null;
           try {
               xxg2 = PersonMsg.Person.parseFrom(input);
           } catch (IOException e) {
               e.printStackTrace();
           }
           System.out.println("ID:" + xxg2.getId());
           System.out.println("name:" + xxg2.getName());
           System.out.println("email:" + xxg2.getEmail());
           System.out.println("friend:");
           List<String> friends = xxg2.getFriendsList();
           for(String friend : friends) {
               System.out.println(friend);
           }
       }
   }
   ```

6. 设置自动生成包名，修改`PersonMsg.proto`文件

   ```protobuf
   //指定编译版本2或3
   syntax = "proto2";
   //当前包名
   package PersonMsg;
   //包路径
   option java_package = "com.exxk.protobuf";
   //类名
   option java_outer_classname = "PersonMsg";
   
   message Person {
   
       // ID（必需）
       required int32 id = 1;
   
       // 姓名（必需）
       required string name = 2;
   
       // email（可选）
       optional string email = 3;
   
       // 朋友（集合）
       repeated string friends = 4;
   }
   
   message car {
   }
   ```

7. 修改命令`.\protobuf\protoc-3.6.1-win32.exe --java_out=.\protobuf\src\main\java\  .\protobuf\src\test\protobuf\PersonMsg.proto`

### protoc gradle插件

插件地址：[google/protobuf-gradle-plugin](https://github.com/google/protobuf-gradle-plugin#latest-version)

1. 在父级`build.gradle`添加

   ```groovy
   buildscript {
     repositories {
       mavenCentral()
     }
     dependencies {
       classpath 'com.google.protobuf:protobuf-gradle-plugin:0.8.8'
     }
   }
   ```

2. 在子项目`build.gradle`添加

   ```groovy
   apply plugin: 'com.google.protobuf'
   
   dependencies {
       compile 'com.google.protobuf:protobuf-java:3.6.1'
   }
   
   sourceSets {
       main {
           proto {
               // In addition to the default 'src/main/proto'
               //proto输入目录
               srcDir 'src/main/protobuf'
               srcDir 'src/main/protocolbuffers'
               srcDir 'src/main/protocol buffers'
               // In addition to '**/*.proto' (use with caution).
               // Using an extension other than 'proto' is NOT recommended, because when
               // proto files are published along with class files, we can only tell the
               // type of a file from its extension.
               include '**/*.protodevel'
           }
       }
       test {
           proto {
               // In addition to the default 'src/test/proto'
               srcDir 'src/test/protocolbuffers'
           }
       }
   }
   protobuf {
       //输出目录
       generatedFilesBaseDir = "$projectDir/src"
       protoc {
           //protoc编译版本
           artifact = 'com.google.protobuf:protoc:3.0.0'
       }
   }
   ```

3. 然后点击右侧gradle`protobuf->Tasks->other->generateProto`编译proto文件生成java文件

### protoc maven插件

解决不同平台开发编译问题，功能能实现自动根据不同系统(os/win/linux)调用不同的protoc工具

### 插件一[os72/protoc-jar-maven-plugin](https://github.com/os72/protoc-jar-maven-plugin)

配置更改一直不生效，一直使用最新的3.6.0版本的protoc工具

### 插件二[org.xolstice.maven.plugins/protobuf-maven-plugin](https://www.xolstice.org/protobuf-maven-plugin/)

[Maven工程处理Protobuf](https://my.oschina.net/u/573325/blog/1617416)

目录结构：

```powershell
├─src
│  ├─main
│  │  ├─java //proto生成java文件目录
│  │  │  └─com
│  │  │      └─surelive
│  │  │          └─app
│  │  │              └─server
│  │  │                  └─protocol
│  │  │                      ├─request  
│  │  │                      └─response
│  │  └─resources 
│  │      └─proto //proto文件目录
│  │          ├─request
│  │          └─response
│  └─test
│      └─java
├─pom.xml
```



编写`pom.xml`添加插件

```xml
<project ...>    
    ....
    <dependencies>
        <dependency>
            <groupId>com.google.protobuf</groupId>
            <artifactId>protobuf-java</artifactId>
            <version>2.5.0</version>
        </dependency>

    </dependencies>

    <build>
        <defaultGoal>package</defaultGoal>
        <!--识别系统类型-->
        <extensions>
            <extension>
                <groupId>kr.motd.maven</groupId>
                <artifactId>os-maven-plugin</artifactId>
                <version>1.6.0</version>
            </extension>
        </extensions>
        <plugins>
            <!-- protobuf 编译组件 -->
            <plugin>
                <groupId>org.xolstice.maven.plugins</groupId>
                <artifactId>protobuf-maven-plugin</artifactId>
                <version>0.6.1</version>
                <extensions>true</extensions>
                <configuration>
                    <!--proto源文件目录-->
                    <protoSourceRoot>${project.basedir}/src/main/proto</protoSourceRoot>
                    <!--输出目录-->
                    <outputDirectory>${project.basedir}/src/main/java</outputDirectory>
                    <!--设置是否在生成java文件之前清空outputDirectory的文件，默认值为true，设置为false时也会覆盖同名文件-->
                    <clearOutputDirectory>true</clearOutputDirectory>
                    <!--编译命令及版本，${os.detected.classifier}识别版本号，依赖os-maven-plugin插件-->
                    <protocArtifact>com.google.protobuf:protoc:2.5.0:exe:${os.detected.classifier}</protocArtifact>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>compile</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

使用，点击右侧插件里面的`protobuf->protobuf:compile`或者执行`mvn protobuf:compile`



##### 注意

1. 不添加输出目录识别不了多级目录（奇怪）
2. 设置目录`protoSourceRoot`目录是，是以该目录为相对路径，因此代码里面的`import "response/xxx.proto`要加上`response`二级目录，但是如果可以设置protoSourceRoot为两个或二级目录就不需要修改，`clearOutputDirectory`设置true，也不会清理其他目录中其他文件

