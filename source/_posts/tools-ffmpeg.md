---
title: tools-ffmpeg
date: 2020-09-09 16:58:53
updated: 2020-09-10 15:03:21
categories: Tools
tags: [Tools,ffmpeg]
---

## 简介

视频转换

[官方文档](https://www.ffmpeg.org/)

[FFmpeg 视频处理入门教程](https://www.ruanyifeng.com/blog/2020/01/ffmpeg.html)

## 常用命令

```bash
#查看视频信息
ffprobe 1.mkv
#播放视频
ffplay 1.mkv
#将字幕封装到mkv视频容器中
ffmpeg -i 1.mkv -i 1.ass -c copy 11.mkv
#设置视频源数据里面的标题
ffmpeg -i 1.mkv -metadata title='标题' -c copy 11.mkv
#复制所有的0开头的流（各种音频字幕流）
ffmpeg -i 1.mkv -c copy -map 0 11.mkv
#复制metadata里面的数据
ffmpeg -i 1.mkv -c copy -map_metadata 0 11.mkv
#整合
ffmpeg -i 1.mkv -i 1.ass -metadata title='标题' -c copy -map 0 -map_metadata 0 11.mkv
ffmpeg -i 1.mkv -i 1.ass -metadata title='小公女セーラ 第01話「ミンチン女子学院」' -c copy -map 0 -map_metadata 0 111.mkv
```

## 基础

```bash
#基础格式
ffmpeg {全局参数} {输入文件参数} -i {输入文件} {输出文件参数} {输出文件}
# eg:
ffmpeg \
-y \ # 全局参数
-c:a libfdk_aac -c:v libx264 \ # 输入文件参数
-i input.mp4 \ # 输入文件
-c:v libvpx-vp9 -c:a libvorbis \ # 输出文件参数
output.webm # 输出文件
ffmpeg -i input.avi output.mp4  #简写
#常用命令行参数
-c：指定编码器
-c copy：直接复制，不经过重新编码（这样比较快）
-c:v：指定视频编码器
-c:a：指定音频编码器
-i：指定输入文件
-an：去除音频流
-vn： 去除视频流
-preset：指定输出的视频质量，会影响文件的生成速度，有以下几个可用的值 ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow。
-y：不经过确认，输出时直接覆盖同名文件。
```

## 安装

```bash
#mac
brew install ffmpeg
```

