---
title: Java-video
date: 2018-08-24 11:16:50
updated: 2018-09-13 17:15:47
categories: Java
tags: [Java,ffmpeg]
---

## java视频监控二次开发

#### 工具环境：

1. [SADP](https://pan.baidu.com/s/1c2OxIwS)设备网络搜索软件：改密，查询海康设备参数型号，访问地址等
2. VLC mdeia player网络视频流测试工具



### 总结

视频设置有两种一种通过硬盘录像机管理所有单个录像摄像头进行直播，二是单个摄像头进行直播流设置



#####  RTSP端口

查看登陆设备：高级->网络->端口->RTSP

应用：

```bash
# 7544 为 RTSP端口，摄像头独立直播流配置
ffmpeg -rtsp_transport tcp -i rtsp://admin:12345@192.168.1.194:7544  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 -f flv rtmp://127.0.0.1:1935/hls/video1
```



##### SDK 端口/服务端口

高级->网络->端口->SDK端口或服务端口

硬盘录像机：服务端口，应用`hikvision_port=2004` 其中2004为服务端口（也叫sdk端口）

摄像头：sdk端口，应用`hikvision_video_username_password2 = 34,192.168.1.193,8000,admin,12345`其中8000为服务端口（也叫sdk端口）



#### 控制原理

![](http://ohdtoul5i.bkt.clouddn.com/1535084718762.png)





### dvr视频录像机统一 做直播预览与回放

```bash
#tracks为回放
#为dvr的ip和rstp端口，其中101 代表通道1主码流01
rtsp://admin:12345@192.168.1.195:5555/Streaming/tracks/101?starttime=20180911t063812z&endtime=20180911t064816z

#Channels为直播
rtsp://admin:12345@192.168.1.195:5555/Streaming/Channels/

#回播推流,报Too many packets buffered for output stream 0:0.，加了-max_muxing_queue_size 1024 转码期间不能播放，强制结束才开始播放，似乎源不能拖动进度条
ffmpeg -rtsp_transport tcp -i "rtsp://admin:12345@192.168.1.195:5555/Streaming/tracks/101?starttime=20180911t063812z&endtime=20180911t064016z" -max_muxing_queue_size 10240 -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 1280x720 -q 10 -f flv "rtmp://127.0.0.1:1935/hls/video7"



```







### 回放下载

回访下载，然后实时播放增长的文件，可以用vlc播放，但是ckplayer播放不了，需要解码，可以用ffmpeg命令，因此做实施解码相对比较麻烦

```java
        NativeLong hPlayback;
        String filename=sFileName+".mp4";
        String flvfilename=sFileName+".flv";
        String savePath=recordStore+filename;

        File file=new File(savePath);
        logger.info("创建目录："+file.getParentFile());
        if (!file.getParentFile().exists()) {
            boolean result = file.getParentFile().mkdirs();
            if (!result) {
                logger.info("创建失败");
            }
        }

        if (file.exists()){
            logger.info("已经在下载了");
            return;
        }

        if( (hPlayback =  hCNetSDK.NET_DVR_GetFileByName(nUserId, sFileName, savePath)).intValue() < 0 ){
            logger.error( "GetFileByName failed. error[%d]\n"+hCNetSDK.NET_DVR_GetLastError());
             return;
        }

        if(!hCNetSDK.NET_DVR_PlayBackControl_V40(hPlayback, hCNetSDK.NET_DVR_PLAYSTART, null,0,null,null))
        {
            logger.error("play back control failed [%d]\n"+hCNetSDK.NET_DVR_GetLastError());
            return;
        }

         if (!ExecuteCodecs.exchangeToFlv(ffmpegBin, savePath,recordStore+ flvfilename)){
             logger.error("mp4 to flv \n");
         }
```

