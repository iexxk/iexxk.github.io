---
title: adb常用操作
date: 2016-08-24 10:58:31
updated: 2020-07-17 11:43:53
categories: Android
tags: [adb,logcat]
---
## 定位adb路径

进入android sdk路径下的platform-tools目录下
```bash
#mac
 ~/Library/Android/sdk/platform-tools
# windows
C:\DevelopmentTools\Android\sdk\platform-tools
```
## 连接设备

```bash
#如果是远程连接执行
./adb connect 192.168.2.162:5555
#查看连接的设备，usb会直接连接
./adb devices
#断开设备
./adb disconnect
#进入设备shell
./adb shell
```
## 常用操作及命令

```bash
#抓取logcat，ctrl+c结束
./adb logcat
#存储所有logcat，Android日志主要分为kernel、radio、event、main这四种log。
./adb logcat -b main -b system -b radio -b events -v time > C:\Users\xuan\Desktop\log.txt
# 向聚集焦点的输入框输入文本(text)内容为hello
./adb shell input text hell0
#tab键的key code是61 --> "KEYCODE_TAB"
./adb shell input keyevent 61
#下载安卓机器上/sdcard/a.txt文件到当前目录
./adb pull /sdcard/a.txt
#上传文件
./adb push a.txt /sdcard/
#安装apk
./adb install a.apk
```



#### 参考

[KEYCODE列表](https://link.jianshu.com/?t=http://www.360doc.com/content/13/0807/13/5224731_305347225.shtml)




