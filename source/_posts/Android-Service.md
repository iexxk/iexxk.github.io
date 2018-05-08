---
title: Android service服务
date: 2016-10-18 10:33:35
updated: 2018-04-25 20:47:32categories: Android
tags: [startService(),bindService(),IntentService]
---
##### startService() 
>* 启动的服务处于“启动的”状态，一旦启动，service就在后台运行，即使启动它的应用组件已经被销毁了
>* 通常started状态的service执行单任务并且==不返回任何结果==给启动者
##### bindService()
>* 一个绑定的service提供一个允许组件与service交互的接口，可以发送请求、获取返回结果，还可以通过夸进程通信来交互（IPC）。
>* ==绑定的service只有当应用组件绑定后才能运行==，多个组件可以绑定一个service，当调用unbind()方法时，这个service就会被销毁了。

###### 注意：==service与activity一样都存在与当前进程的主线程中==，所以，一些阻塞UI的操作，比如耗时操作不能放在service里进行，比如另外开启一个线程来处理诸如网络请求的耗时操作。
##### IntentService
>* IntentService使用队列的方式将请求的Intent加入队列，然后开启一个worker thread(线程)来处理队列中的Intent，对于异步的startService请求，IntentService会处理完成一个之后再处理第二个，每一个请求都会在一个单独的worker thread中处理，==不会阻塞应用程序的主线程==
#### 参考
[Android service服务-张雪源的博客](http://qushouxichuan.com/blog/article/51)