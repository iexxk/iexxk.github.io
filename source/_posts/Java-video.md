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
ffmpeg -rtsp_transport tcp -i rtsp://admin:12345@192.0.0.63:554/h264/ch1/main/av_stream  -vcodec copy -acodec aac -ar 44100 -strict -2 -ac 1 -f flv -s 704x576 -q 10 -f flv rtmp://127.0.0.1:1935/hls/video1
```



##### SDK 端口/服务端口

高级->网络->端口->SDK端口或服务端口

硬盘录像机：服务端口，应用`hikvision_port=2004` 其中2004为服务端口（也叫sdk端口）

摄像头：sdk端口，应用`hikvision_video_username_password2 = 34,192.168.1.193,8000,admin,12345`其中8000为服务端口（也叫sdk端口）



#### 控制原理

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/1535084718762.png)





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









#### [海康录像机RTSP取流路径](http://haikang.faqrobot.cn/servlet/WXShow?action=sac&wxcId=63&sysNum=145716889796196&FromUserName=oNNCAjviKiFIfdX5IhEPUmQzP8Vg&sId=236075&subId=218733)

2012年之前的设备支持老的取流格式，之后的设备新老取流格式都支持。

【老URL，小于64路的NVR或混合录像机的IP通道从33开始；大于等于64路的NVR的IP通道从1开始】



`rtsp://username:password@<ipaddress>/<videotype>/ch<number>/<streamtype>`

**详细描述：**

**![blob.png](http://haikang.faqrobot.cn/upload/web/145716889796196/20170808/71391502161074550.png)**

 **举例说明：**

DS-9016HF-ST的IP通道01主码流：

rtsp://admin:12345@172.6.22.106:554/h264/ch33/main/av_stream

DS-9016HF-ST的模拟通道01子码流：

rtsp://admin:12345@172.6.22.106:554/h264/ch1/sub/av_stream

【新URL，通道号全部按顺序从1开始】

**详细描述：**

`rtsp://username:password@<address>:<port>/Streaming/Channels/<id>(?parm1=value1&parm2-=value2…)`

![blob.png](http://haikang.faqrobot.cn/upload/web/145716889796196/20170808/86951502161663245.png)

**举例说明：**

DS-9632N-ST的IP通道01主码流，：

rtsp://admin:12345@172.6.22.234:554/Streaming/Channels/101

DS-9632N-ST的IP通道01子码流：

rtsp://admin:12345@172.6.22.234:554/Streaming/Channels/102

 