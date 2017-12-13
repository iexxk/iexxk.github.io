---
title: Retrofit学习之一介绍
date: 2016-08-25 12:52:21
categories: Retrofit
tags: [网络框架,Retrofit]
---
# 认识
当前的网络开源库有许多，如volley，okhttp，retrofit等，这三个库当前是比较火的，其中，okhttp和retrofit由square团队开发。
>* okhttp是高性能的http库，等同于httpclient,6.0将替换httpclient
>* 简化了网络请求流程，同时自己内部对OkHtttp客户端做了封装
>* gson库是为了将返回数据转化为实体类

# 搭建环境
### [Retrofit](http://square.github.io/retrofit/)
```
compile 'com.squareup.retrofit2:retrofit:2.1.0'
```
### gson
```
//将请求结果转换成json的json转换包，如果导入了这个依赖，就不用再导入Gson包，因为这个已经包含了Gson包
compile 'com.squareup.retrofit2:converter-gson:2.1.0'
```
### 网络权限
```xml
<!-- 用于访问网络，网络定位需要上网 -->
<uses-permission android:name="android.permission.INTERNET" />
```
 