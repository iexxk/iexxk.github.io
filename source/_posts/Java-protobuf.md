---
title: Java-protobuf
date: 2019-02-15 15:39:21
updated: 2019-02-16 20:57:36
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

### protoc maven插件

解决不同平台开发编译问题，功能能实现自动根据不同系统(os/win/linux)调用不同的protoc工具

### 插件一[os72/protoc-jar-maven-plugin](https://github.com/os72/protoc-jar-maven-plugin)

配置更改一直不生效，一直使用最新的3.6.0版本的protoc工具

### 插件二[org.xolstice.maven.plugins/protobuf-maven-plugin](https://www.xolstice.org/protobuf-maven-plugin/)