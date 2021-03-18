---
title: RxJava之操作符(2)
date: 2016-09-18 11:21:58
updated: 2021-03-18 18:04:32
categories: RxJava
tags: [Rxjava,操作符]
---

### 参考网址
>* [Android RxJava使用介绍](http://blog.csdn.net/Job_Hesc/article/category/2919759)
>* [RxJava](http://blog.csdn.net/u010163442/article/category/6270573)
>* [RxJava官方文档](http://reactivex.io/documentation/operators.html)

### 使用过的操作符
>* **`concat`** 连接多个Observables(被观察者)
>  ![concat](https://s3.ax1x.com/2021/03/18/62hShj.png)
>  最多有9个参数，但是可以嵌套，传的数据必须是相同类型
>* **`mergeDelayError`** 合并发送
>  ![MergeDelayError](https://s3.ax1x.com/2021/03/18/62hK3R.png)
>  合并两个发送，如果一个出错不马上发送错误，而是延时到都发送完
>* **`interval`** 定时循环发送
>  ![interval](https://s3.ax1x.com/2021/03/18/62h8HO.png)
>* **`map`** 数据类型转换(同步)
>  ![map](https://s3.ax1x.com/2021/03/18/62hUCd.png)
>* **`flatmap`** 传入数据，生成新的Observable，一般处理异步任务，连接能实现concat功能
>  ![flatmap](https://s3.ax1x.com/2021/03/18/62hwvt.png)
>* **`distinct`** 过滤去重操作符
>  ![distinct](https://s3.ax1x.com/2021/03/18/62h6Ug.png)
>* **`distinct(Func1)`** 自定义过滤操作符
>  ![distintF1](https://s3.ax1x.com/2021/03/18/62hR8s.png)
>  可以以其中的某个重复项为过滤条件
>* **`repeat`** 重复发送
>  ![repeat](https://s3.ax1x.com/2021/03/18/624pVO.png)
>  重复订阅
>* **`retry`** 错误重试
>  ![retry](https://s3.ax1x.com/2021/03/18/6249aD.png)
>  发送一个错误(onError),重新订阅
>* **`retryWhen(Func1)`** 判断错误，根据错误(func1)决定是否重新订阅
>  ![retryWhen](https://s3.ax1x.com/2021/03/18/62hxr6.png)
>  发送一个错误(onError),通过func1处理错误，决定是否再次订阅
>* **`Timeout`** 超时发送一个onError
>  ![Timeout](https://s3.ax1x.com/2021/03/18/62hzqK.png)
>* **`zip`** 组合
>  ![zip](https://s3.ax1x.com/2021/03/18/62hvKx.png)
>* **`zipwith`** 组合
>  ![zipwith](https://s3.ax1x.com/2021/03/18/624CIe.png)
>  两个都发送onnext后组合，如果另外一个未发，等待组合后才开始发下一个
>* **`delay`**  延时发送
>  ![delay](https://s3.ax1x.com/2021/03/18/624iPH.png)
