---
title: Other-video-h5
date: 2019-11-20 20:42:01
updated: 2020-03-04 16:53:16
categories: 杂谈
tags: [rtsp]
---

## 视频直播解决方案

### 方案一ffmpeg+nginx(rtmp/hls)

rtmp解决方案大众，但是依赖adobe flash player

hls延时高

### 方案二ffmpeg+webSocket

原理ffmpeg解码转流(图片)，webSocket接收，然后前端画布按帧绘制

```bash
#拉去代码https://github.com/phoboslab/jsmpeg
git clone git@github.com:phoboslab/jsmpeg.git
#进入项目目录执行
npm install ws
#运行JSMpeg，8081为ffmpeg推流端口，8082为websocket端口
node websocket-relay.js supersecret 8081 8082
#运行转码推流
ffmpeg -i rtsp://admin:admin@10.30.11.119:554/h264/ch1/main/av_stream -q 0 -f mpegts -codec:v mpeg1video -s 352x240 http://10.30.11.40:8081/supersecret
```

修改`view-stream.html`

```html
<!DOCTYPE html>
<html>
<head>
	<title>JSMpeg Stream Client</title>
	<style type="text/css">
		html, body {
			background-color: #111;
			text-align: center;
		}
	</style>
</head>
<body>
	<canvas id="video-canvas"></canvas>
	<script type="text/javascript" src="jsmpeg.min.js"></script>
	<script type="text/javascript">
		var canvas = document.getElementById('video-canvas');
		var url = 'ws://10.30.11.150:8082/';
		var player = new JSMpeg.Player(url, {canvas: canvas});
	</script>
</body>
</html>

```

#### 测试

访问静态网页

[file:///Users/xuanleung/Downloads/jsmpeg-master/view-stream.html](file:///Users/xuanleung/Downloads/jsmpeg-master/view-stream.html)



### 参考

[html5播放rtsp方案](https://my.oschina.net/chengpengvb/blog/1832469?p=3)

[phoboslab/jsmpeg](https://github.com/phoboslab/jsmpeg)