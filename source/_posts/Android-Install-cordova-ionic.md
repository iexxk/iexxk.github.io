---
title: android混合开发-环境搭建
date: 2017-03-08 15:02:45
updated: 2018-01-28 21:41:27categories: Android
tags: [混合开发、android、cordova]
---
#### 环境搭建

1. 下载[nodejs](https://nodejs.org/en/),并安装，安装过程默认（可修改[路径](C:\Develop\nodejs)）,成功校验(`npm -version`)

   Javascript的运行环境,这里主要使用npm附属插件（包管理）

2. `npm install -g cordova`  安装[cordova](http://cordova.apache.org/)

   混合开发环境，Cordova提供了js和原生API的调用接口，通过插件，我们可以实现例如拍照，扫码等操作； 并且提供了静态文件转换成APP的功能。

3. `npm install -g cordova ionic`安装[ionic](http://ionicframework.com/)

   Ionic 是基于 Cordova 的，在 Cordova 上能用的一切同样可以在 Ionic 上使用
   Ionic 在 Cordova 基础上增加了 Ionic UI、AngularJS、一个强大的 CLI 工具和一些云端服务等

4. ​