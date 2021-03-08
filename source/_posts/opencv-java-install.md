---
title: OpenCV-java-install
date: 2018-04-21 13:37:43
updated: 2018-12-12 10:47:58
categories: OpenCV
tags: [OpenCV,java,install]
---

#### [mac开发环境](https://opencv-java-tutorials.readthedocs.io/en/latest/01-installing-opencv-for-java.html#install-opencv-3-x-under-macos)

1. 环境准备

   ```bash
   # 安装开发基本组件（一般都安装了）可以跳过
   xcode-select --install
   # 安装ant，这里是使用Homebrew进行安装，为了方便管理
   brew install ant
   # 编辑配置文件(其实就vim编辑配置文件)
   brew edit opencv
   >修改为 -DBUILD_opencv_java=ON
   # 最后安装opencv，依赖于python2，可以提前建好，也可以通过依赖的方式自动安装
   brew install --build-from-source opencv
   ```

2. 安装成功后jar包位于`/usr/local/Cellar/opencv/3.x.x/share/OpenCV/java/`

3. idea设置vm启动参数`-Djava.library.path=/usr/local/Cellar/opencv/3.4.3/share/OpenCV/java/`

##### 问题

1. `Permission denied @ dir_s_mkdir`

   解决：重建目录

   ```bash
   sudo mkdir /usr/local/Frameworks
   sudo chown $(whoami):admin /usr/local/Frameworks
   # 测试
   brew link python
   ```








idea+springboot+opencv3.4.1+alpine

#### 安装

由于alpine apk add opencv 运行报错，等待opencv出正式版

等待升级中。。。。。。。



opencv_java341.dll

[](http://www.voidcn.com/article/p-ksqbxwed-bnz.html)

