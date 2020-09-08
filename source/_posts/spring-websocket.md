---
title: Spring-WebSocket
date: 2019-06-12 10:29:40
updated: 2020-09-08 11:43:41
categories: Spring
tags: [WebSocket]
---

## 基础

### 工具

服务器

下载[http://websocketd.com/](http://websocketd.com/)

添加脚本`count.sh`然后添加权限`chmod +x count.sh`

```
#!/bin/bash
for ((COUNT = 1; COUNT <= 10; COUNT++)); do
  echo $COUNT
  sleep 1
done
```

启动` ./websocketd --port=8080 ./count.sh`服务端

客户端

https://jsbin.com/zemigup/edit?js,console在该网页运行下面的脚本

```js
var ws = new WebSocket("ws://127.0.0.1:8080");

ws.onopen = function(evt) { 
  console.log("Connection open ..."); 
  ws.send("Hello WebSockets!");
};

ws.onmessage = function(evt) {
  console.log( "Received Message: " + evt.data);
  ws.close();
};

ws.onclose = function(evt) {
  console.log("Connection closed.");
};      
```

上面不支持非127.0.0.1的，测试ws://10.30.6.10:8080需要在[http://www.blue-zero.com/WebSocket/](http://www.blue-zero.com/WebSocket/)测试





## 参考

[官网](https://spring.io/guides/gs/messaging-stomp-websocket/)

[WebSocket 教程-阮一峰]([http://www.ruanyifeng.com/blog/2017/05/websocket.html](http://www.ruanyifeng.com/blog/2017/05/websocket.html))