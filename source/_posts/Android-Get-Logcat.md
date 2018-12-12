---
title: Android抓Logcat
date: 2016-08-24 10:58:31
updated: 2018-12-12 10:47:58categories: Android
tags: [adb,logcat]
---
# 定位adb的路径
在android sdk路径下的platform-tools目录下
```
C:\DevelopmentTools\Android\sdk\platform-tools>cd C:\DevelopmentTools\Android\sdk\platform-tools
```
# 检测设备
```
C:\DevelopmentTools\Android\sdk\platform-tools>adb devices
```
# 抓取logcat
```
C:\DevelopmentTools\Android\sdk\platform-tools>adb logcat
```
停止按ctrl+c
# 存储所有logcat
```
C:\DevelopmentTools\Android\sdk\platform-tools>adb logcat -b main -b system -b radio -b events -v time > C:\Users\xuan\Desktop\log.txt
```
# Log分类
Android日志主要分为kernel、radio、event、main这四种log。


