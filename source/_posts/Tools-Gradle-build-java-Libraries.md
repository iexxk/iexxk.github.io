---
title: Gradle构建java库
date: 2018-05-13 16:41:51
updated: 2018-12-12 10:47:58
categories: Tools
tags: [Gradle,java]
---

`gradle init --type <name>`其中name可选

* java-application
* java-library
* scala-library
* groovy-library
* basic

## build java-library

> This guide walks you through the process of using Gradle’s Build Init plugin to produce a JVM library which is suitable for consumption by other JVM libraries and applications.

本指南引导您完成使用Gradle的Build Init插件生成适合其他JVM库和应用程序使用的JVM库的过程。

```bash
mkdir demo-java-lib #创建项目目录
cd demo-java-lib
gradle init --type java-library  #初始化构建为java-library
tree #查看生成的目录树
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
    ├── main  #java资源为件
    │   └── java  
    │       └── Library.java
    └── test  #java测试文件
        └── java
            └── LibraryTest.java

```

`build.gradle`解读

```groovy
plugins {
    // Java Library依赖插件
    id 'java-library'
}
dependencies {
    // 依赖该api
    api 'org.apache.commons:commons-math3:3.6.1'
    implementation 'com.google.guava:guava:23.0'
    testImplementation 'junit:junit:4.12'
}
repositories {
    // 仓库
    jcenter()
}
```

执行`./gradew build`第一次构建会下载依赖jar包比较慢,下载到目录`~/.gradle/wrapper/dists`，编译完成后生成

* build/reports/tests/test/index.html 测试报告
* build/libs/building-java-libraries.jar 编译生成的jar

`jar tf build/libs/building-java-libraries.jar`命令查看jar包内容，其中`-f`指定jar文件名，`-t`列出包的内容

修改`build.gradle`文件在文件里添加版本好`version = '0.1.0'`，结果会修改打包的名称为`build/libs/demo-java-lib-0.1.0.jar`

修改`build.gradle`文件在文件里添加`jar` task任务

```
jar {
    manifest {
        attributes('Implementation-Title': project.name,
                   'Implementation-Version': project.version)
    }
}
```

会修改`build/libs/building-java-libraries-0.1.0.jar/META-INF/MANIFEST.MF`jar包文件的内容为

```properties
Manifest-Version: 1.0
Implementation-Title: demo-java-lib
Implementation-Version: 0.1.0
```

java-library内置支持javadoc，执行`./gradlew javadoc`会生成`/build/docs/javadoc/index.html`文档

## build java-application

java项目和library项目一样，只是多了tasks任务 run