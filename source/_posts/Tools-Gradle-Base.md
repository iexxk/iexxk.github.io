---
title: Tools-Gradle-Base
date: 2018-05-10 16:58:41
updated: 2018-05-11 18:04:57
categories: Tools
tags: [Gradle]
---

## [安装Gradle](https://gradle.org/install/)

1. java环境必须
2. 下载[Gradle](https://gradle.org/releases/),其中binary-only为单独的安装包，complete为文档加安装包，然后解压
3. 在path中添加系统环境变量`F:\xuan\gradle-4.7\bin`
4. 执行`gradle -v`检查是否安装成功

## 使用Gradle

1. 进入一个Gradle项目,或者拉取一个` git clone git@github.com:gradle/gradle-build-scan-quickstart.git`

### Gradle build scans使用

> Build Scans是用于开发和维护Gradle构建的重要工具。它为你提供了构建的详细信息，并为你识别构建环境、依赖或性能上存在的问题，同时可以帮你更全面地理解并提升构建过程，也便于与他人的合作。

大概理解就是该插件能把构建过程的数据分享出去，方便让别人查看分析构建信息。

1. 进入项目跟目录执行构建扫描命令`./gradlew build --scan`，有可能会提示`Do you accept these terms?`是否接受许可协议，输入yes即可，成功后日志会输出一个链接类似https://scans.gradle.com/s/z5i6rmnpd4sbu，访问该链接就可以查看构建日志信息了（有的打开也许需要邮箱）。

2. 上面虽然得到了链接，但是可以直接在`build.gradle`添加相关配置信息，构建扫描插件[build-scan](https://plugins.gradle.org/plugin/com.gradle.build-scan),为了将构建扫码发布到https://gradle.com/terms-of-service需要接受协议

   ```
   plugins {
       id 'com.gradle.build-scan' version '1.13.2' //如果是低版本一定要放到其他插件前面
   }
   //配置扫描发送地址，以及同意协议
   buildScan {
       termsOfServiceUrl = 'https://gradle.com/terms-of-service'
       termsOfServiceAgree = 'yes'  //同意协议
   	tag 'xuan test'  //打标签
   	//项目的地址，这里需要是http地址，用git开头的地址编译报错
   	link 'GitHub','https://github.com/gradle/gradle-build-scan-quickstart'
   }
   ```

3. 执行`gradle build -Dscan`运行得到链接，然后访问即可

### Creating New Gradle Builds

##### 初始化gradle 项目

```powershell
mkdir gradle-demo #创建项目目录
cd gradle-demo #进入项目目录
gradle init #初始化为gradle项目
#生成如下目录文件
.
├── build.gradle   #项目配置脚本
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar  #wrapper可执行jar
│       └── gradle-wrapper.properties  #wrapper 配置文件
├── gradlew  # unix systems（linux）系统下的脚本
├── gradlew.bat  # window 下的脚本
└── settings.gradle  #配置那些项目参与构建脚本
```

##### 创建task任务名叫`copy`

```groovy
task copy(type: Copy, group: "Custom", description: "复制src目录到dest目录") {
    from "src"   //前提需要有src目录
    into "dest"  //不需要创建，会自动创建
}
```

命令行执行`./gradlew copy`代表执行task里的copy任务

##### Gradle 应用插件

[插件仓库](https://plugins.gradle.org/)

这里以base插件，base插件功能主要是打包为zip文件

```groovy
plugins {   //这个代码快必须放顶部
	id "base"
}
task copy(type: Copy, group: "Custom", description: "复制src目录到dest目录") {
    from "src"
    into "dest"
}
task zip(type: Zip, group: "Util", description: "压缩src目录文件") {
	from "src"
}
```

执行`./gradlew zip`,然后在目录  `.\build\distributions`下就可以看到`gradle-demo.zip`文件了

##### 常用命令

```powershell
./gradlew tasks #查看可用的task任务
./gradlew zip --scan  #结合scan执行zip，分析执行信息
./gradlew properties #查看可用的配置属性，类似环境变量(配置属性)的
```

在`build.gradle`可以更改`properties`变量的值，但是不能新增，例如修改项目描述和版本号

```groovy
//放在build.gradle文件中，但是不能放在plugins前面，因为plugins这个必须在顶部
description = "该项目为测试学习用"
version = "1.0"
```



## 手册

[Gradle 命令手册](https://docs.gradle.org/4.7/userguide/command_line_interface.html)

### 注意事项

不能在gradle项目的子目录执行`gradle init`

