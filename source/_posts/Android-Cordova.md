---
title: Android-Cordova
date: 2018-04-24 10:51:59
updated: 2018-04-25 20:47:32
categories: Android
tags: [Android,Cordova]
---

## Cordova环境搭建

混合开发环境，Cordova提供了js和原生API的调用接口，通过插件，我们可以实现例如拍照，扫码等操作； 并且提供了静态文件转换成APP的功能。

步骤：

1. 安装[nodejs](https://nodejs.org/zh-cn/)

2. 安装cordova执行`npm install -g cordova`

3. 在工作空间目录执行`cordova create MyApp`创建一个Cordova项目

4. 切换进入刚刚创建的项目跟目录`cd MyApp`

5. `cordova platform`查看该项目可用的平台和已安装的平台

   ```powershell
   Installed platforms:
     android 7.0.0
   Available platforms:
     browser ~5.0.1
     ios ~4.5.4
     osx ~4.0.1
     windows ~5.0.0
     www ^3.12.0
   ```

6. 如果没有安装，添加一个平台`cordova platform add android`

7. 添加Android sdk系统环境变量三个

   ```properties
   JAVA_HOME:C:\Program Files\Java\jdk1.8.0_131
   ANDROID_HOME:F:\xuan\sdk
   PATH:%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools;
   ```

8. 然后执行`cordova requirements`检查相关环境，如果失败，环境变量配置有问题，这里需要注意，环境变量配置了要重启终端，才会生效

   ```properties
   Android Studio project detected

   Requirements check results for android:
   Java JDK: installed 1.8.0
   Android SDK: installed true
   Android target: installed android-27,android-26,android-25,android-24,android-23,android-22
   Gradle: installed C:\Program Files\Android\Android Studio\gradle\gradle-4.1\bin\gradle
   ```

9. 然后执行`cordova build android`编译项目

10. 然后执行`cordova run android`运行项目，需要连接Android设备，如果是模拟器执行`cordova emulate android`

## Cordova 实例

### 调用相机demo

1. 顺序执行下面的命令

   ```powershell
   cordova create cameraDemo #创建cameraDemo相机demo
   cd cameraDemo #进入工程目录
   cordova platform add android #添加android
   cordova plugin add cordova-plugin-camera #添加相机组件
   ```

2. 在上面步骤生成应用的目录，修改`www`目录下的`index.html`

   ```html
     <script type="text/javascript" src="cordova.js"></script>
           <script type="text/javascript" src="js/index.js"></script>
   <button id = "camera">调用相机</button>
   <button id = "wxlogin">微信</button>
   ```

3. 修改`www\js`目录下的`index.js`

   ```js

   var app = {
       initialize: function() {
           document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
   	    document.getElementById("camera").addEventListener("click", this.wxloginEvent);
       },
   	 wxloginEvent: function(){
   		// alert('触发了');
   		navigator.camera.getPicture(onSuccess,onFail,{ 
   			quality: 50,
   			destinationType: Camera.DestinationType.DATA_URL
   		});

   	   function onSuccess(imageData) {
   		  var image = document.getElementById('myImage');
   		  image.src = "data:image/jpeg;base64," + imageData;
   	   }
   	   function onFail(message) {
   		  alert('Failed because: ' + message);
   	   }
   	},
       onDeviceReady: function() {
           this.receivedEvent('deviceready');
       },
       receivedEvent: function(id) {
           var parentElement = document.getElementById(id);
           var listeningElement = parentElement.querySelector('.listening');
           var receivedElement = parentElement.querySelector('.received');

           listeningElement.setAttribute('style', 'display:none;');
           receivedElement.setAttribute('style', 'display:block;');
           console.log('Received Event: ' + id);
       }
   };
   window.onload=function(){   //注意添加此方法包裹，不然会还没加载就调用方法而报错
   	app.initialize();
   }
   ```
4. 执行`cordova run android`运行项目，需要连接Android设备



#### 常见问题

   浏览器打开提示`www/cordova.js net::ERR_FILE_NOT_FOUND`此错误，但是打包Android不会出现





