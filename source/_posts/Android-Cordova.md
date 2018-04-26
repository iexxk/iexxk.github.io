---
title: Android-Cordova
date: 2018-04-24 10:51:59
updated: 2018-04-26 18:30:52
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


### Cordova 加载远程HTML(`修改了html，一定要清除app的缓存`)

上面已经成功创建了一个相机demo，但是他是读取的本地网页，下面记录访问远程html

先分析下生成的目录结构

```js
|cordovaDemo  //跟目录
├─hooks
├─node_modules  //模块
│  ├─cordova-android  //Android设备
│  ├─cordova-plugin-barcodescanner
│  ├─cordova-plugin-compat
│  └─cordova-plugin-whitelist
├─platforms  //设备目录
│  └─android  //Android源码
│      ├─assets
│      │  └─www  //html资源目录，要在远程运行需要把此目录放到远程目录，改相应的配置文件
│      ├─CordovaLib  //Cordova 依赖
│      ├─res
│          ├─xml─config.xml  //修改里面的<content src="url地址" /> 默认是index.html
│      └─src //Android java源文件
├─plugins //插件目录
│  ├─cordova-plugin-barcodescanner
│  ├─cordova-plugin-compat
│  └─cordova-plugin-whitelist
├─res
└─www  //网页源文件，修改之后，build(run)会改变android-assets
```

1. 在上面相机demo运行完项目后，用as打开生成的Android的项目(`.\platforms\android`)

2. 复制`.\platforms\android\assets`目录下的源码到服务器上运行，**注意idea复制包名有可能丢失**

3. 修改Android项目下的`res\xml\config.xml`配置文件

   ```xml
   <!--<content src="index.html" />-->
   <content src="http://112." />    //服务器地址
   ```

4. 如果要制作个android外壳，还需要解决webview跳出到浏览器的问题，修改`CordovaLib\java\...\engine\SystemWebViewClient`下的

   ```java
   @Override
   public boolean shouldOverrideUrlLoading(WebView view, String url) {
       // return parentEngine.client.onNavigationAttempt(url); //注释这句
       return false; //添加这句，具体可以详查webview的使用
   }
   ```

5.  直接在as里面运行Android项目，如果用`cordova run android`运行会覆盖修改掉的东西


### 文档资源

[官网cordova](https://cordova.apache.org/)

[cordova plugins](https://cordova.apache.org/plugins/)


#### 常见问题

1. 浏览器打开提示`www/cordova.js net::ERR_FILE_NOT_FOUND`此错误，但是打包Android不会出现

2. 安装插件：

   ```
   Plugin doesn't support this project's cordova-android version. cordova-android: 7.0.0, failed version requirement:
         <6.3.0
   Skipping 'cordova-plugin-compat' for android
   ```

   解决执行`cordova platform rm android`和`cordova platform remove android`然后安装`cordova platform add android@6.2.0`
