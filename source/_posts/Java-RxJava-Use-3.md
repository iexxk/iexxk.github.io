---
title: RxJava之操作符常用场景(3)
date: 2016-11-29 09:20:16
updated: 2018-04-25 20:47:32categories: RxJava
tags: [RxJava,操作符,使用场景]
---
### 定时心跳

###### 场景描述：
1. 一个发送数据出口
2. 定时循环发送一个数据
3. 当需要发送一个数据临时插入一个数据从出口发送

###### 需要用到的操作符
`repat` 重复发送
`delay` 延时发送 
`just` 快速创建被观察者，插入心跳数据
`mergeDelayError` 合并发送，错误延时

###### 流程
主要是创建两个被观察者，一个负责心跳的发送，另外一个负责数据的发送

###### 实现代码
```java
       Observable alive=Observable.just(temp_send).delay(4000,TimeUnit.MILLISECONDS).repeat(); //心跳数据（每隔4s重复发一次）
       Observable send=  Observable.create(new Observable.OnSubscribe<byte[]>() {
            @Override
            public void call(Subscriber<? super byte[]> subscriber) {
                subscriberSend=subscriber;   //负责数据的发送
            }
        });
        //合并，订阅
       send_subscribe= Observable.mergeDelayError(alive,send).subscribe(new Action1<byte[]>() {
            @Override
            public void call(byte[] bs) {
                send(bs);  //数据出口
            }
        });
```

### 重复执行某个动作直到成功，或失败，或超时

###### 场景描述：
1. 重复执行某个动作
2. 成功后中断继续执行操作
3. 错误继续执行
4. 未响应发出超时错误，并继续执行
5. 达到超时次数，终止执行

###### 需要用到的操作符
`distinct` 过滤
`timeout` 超时发出错误
`retryWhen` 错误重试
`zipWith` 合并（用于统计错误重试次数）
`delay` 延时（用于发送错误后等待一段时间继续发送）

###### 流程
发出动作请求，等待结果，过滤结果。
1. 结果为onError立马重新发出动作请求
2. 等待指定时间没有结果，发出超时onError然后重新发出动作请求
3. 结果为成功结果终止动作请求
4. 直到成功为止，或者超过重试的指定次数

###### 实现代码
```java
    public Observable<String> xuanSend(final String str){
        return Observable.create(new Observable.OnSubscribe<String>() {
            @Override
            public void call(Subscriber<? super String> subscriber) {
                Log.d("TASK_SHOW","任务："+str+"，状态：开始执行，发送数据：空");
                strTask=str;
                subscriber.onNext(str+"中......");
                subscriberTask=subscriber;   //执行结果的入口

            }
        }).distinct().timeout(5000,TimeUnit.MILLISECONDS).retryWhen(new Func1<Observable<? extends Throwable>, Observable<?>>() {
            @Override
            public Observable<?> call(final Observable<? extends Throwable> observable) {
                return observable.zipWith(Observable.range(1, 5), new Func2<Throwable, Integer, Object>() {
                    @Override
                    public Object call(Throwable throwable, Integer integer) {
                        if(throwable.getMessage()==null)
                            Log.d("TASK_SHOW","任务："+str+"，状态：异常结束，异常："+"第"+integer+"次,执行超时");
                        else
                            Log.d("TASK_SHOW","任务："+str+"，状态：异常结束，异常："+throwable.getMessage());
                        return 0;
                    }
                }).delay(10000,TimeUnit.MILLISECONDS);
            }
        });
    }
```

### 任务流(循环)

###### 场景描述
1. 一个动作完成后才执行下一个动作
2. 所有动作完成后重复继续执行

###### 需要用到的操作符
`concat` 连接操作符（只能连接9个，但是可以嵌套）
`repat` 循环

###### 流程
使用flatmap创建一个基本异步任务，用concat实现连接，用reapt实现循环

###### 实现代码
```java
//任务流
  Observable<String> task=Observable.concat(mBle.connet(bleDevicesList.getmBleDevicesList_test()),mBle.enableRX(),mBle.xuanSend(sendData.setStart(false),Ble.START),mBle.xuanSend(sendData.setsafe(false,false),Ble.CANCELSAFE),mBle.disConnet());
                
	task.repeat().subscribeOn(Schedulers.computation()).observeOn(AndroidSchedulers.mainThread()).subscribe(new Subscriber<String>() {
                    @Override
                    public void onCompleted() {
						//所有任务完成，但是如果reapt（）,始终是不会完成的
					   }
                    @Override
                    public void onError(Throwable e) {
                       //发生错误时
                    }
                    @Override
                    public void onNext(String result) {
                       //任务完成
                    }

                });
```


