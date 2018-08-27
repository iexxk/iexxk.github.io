---
title: Java-video
date: 2018-08-24 11:16:50
updated: 2018-08-26 23:27:31
categories: Java
tags: [Java,ffmpeg]
---

## java视频监控二次开发

#### 工具环境：

1. [SADP](https://pan.baidu.com/s/1c2OxIwS)设备网络搜索软件：改密，查询海康设备参数型号，访问地址等
2. VLC mdeia player网络视频流测试工具



#####  RTSP端口

查看登陆设备：高级->网络->端口->RTSP

应用：

```bash
# 7544 为 RTSP端口
ffmpeg -rtsp_transport tcp -i rtsp://admin:12345@192.168.1.194:7544  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 -f flv rtmp://127.0.0.1:1935/hls/video1
```



##### SDK 端口/服务端口

高级->网络->端口->SDK端口或服务端口

硬盘录像机：服务端口，应用`hikvision_port=2004` 其中2004为服务端口（也叫sdk端口）

摄像头：sdk端口，应用`hikvision_video_username_password2 = 34,192.168.1.193,8000,admin,12345`其中8000为服务端口（也叫sdk端口）



#### 控制原理

![](http://ohdtoul5i.bkt.clouddn.com/1535084718762.png)

