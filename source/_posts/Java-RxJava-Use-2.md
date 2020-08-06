---
title: RxJava之操作符(2)
date: 2016-09-18 11:21:58
updated: 2020-08-06 09:51:26
categories: RxJava
tags: [Rxjava,操作符]
---

### 参考网址
>* [Android RxJava使用介绍](http://blog.csdn.net/Job_Hesc/article/category/2919759)
>* [RxJava](http://blog.csdn.net/u010163442/article/category/6270573)
>* [RxJava官方文档](http://reactivex.io/documentation/operators.html)

### 使用过的操作符
>* **`concat`** 连接多个Observables(被观察者)
>  ![concat](http://gt163.cn:14033/blog/20200806094504.png)
>  最多有9个参数，但是可以嵌套，传的数据必须是相同类型
>* **`mergeDelayError`** 合并发送
>  ![MergeDelayError](http://gt163.cn:14033/blog/20200806094608.png)
>  合并两个发送，如果一个出错不马上发送错误，而是延时到都发送完
>* **`interval`** 定时循环发送
>  ![interval](http://gt163.cn:14033/blog/20200806094634.png)
>* **`map`** 数据类型转换(同步)
>  ![map](http://gt163.cn:14033/blog/20200806094702.png)
>* **`flatmap`** 传入数据，生成新的Observable，一般处理异步任务，连接能实现concat功能
>  ![flatmap](http://gt163.cn:14033/blog/20200806094731.png)
>* **`distinct`** 过滤去重操作符
>  ![distinct](http://gt163.cn:14033/blog/20200806094805.png)
>* **`distinct(Func1)`** 自定义过滤操作符
>  ![distintF1](http://gt163.cn:14033/blog/20200806094818.png)
>  可以以其中的某个重复项为过滤条件
>* **`repeat`** 重复发送
>  ![repeat](http://gt163.cn:14033/blog/20200806094856.png)
>  重复订阅
>* **`retry`** 错误重试
>  ![retry](http://gt163.cn:14033/blog/20200806094920.png)
>  发送一个错误(onError),重新订阅
>* **`retryWhen(Func1)`** 判断错误，根据错误(func1)决定是否重新订阅
>  ![retryWhen](http://gt163.cn:14033/blog/20200806094941.png)
>  发送一个错误(onError),通过func1处理错误，决定是否再次订阅
>* **`Timeout`** 超时发送一个onError
>  ![Timeout](http://gt163.cn:14033/blog/20200806095004.png)
>* **`zip`** 组合
>  ![zip](http://gt163.cn:14033/blog/20200806095033.png)
>* **`zipwith`** 组合
>  ![zipwith](http://gt163.cn:14033/blog/20200806095049.png)
>  两个都发送onnext后组合，如果另外一个未发，等待组合后才开始发下一个
>* **`delay`**  延时发送
>  ![delay](http://gt163.cn:14033/blog/20200806095115.png)
