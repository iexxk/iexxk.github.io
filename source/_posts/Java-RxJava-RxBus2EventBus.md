---
title: RxJava之RxBus替代EventBus
date: 2016-09-28 11:32:22
updated: 2018-04-25 20:47:32categories: RxJava
tags: [RxJava,总线,EventBus,RxBus]
---
### 参考
* [RxBus 的简单实现](http://brucezz.itscoder.com/articles/2016/06/02/a-simple-rxbus-implementation/)
* [用RxJava实现事件总线(Event Bus)](http://www.jianshu.com/p/ca090f6e2fe2/)

#### 创建RxJava.java
```java
public class RxBus {
    private static volatile RxBus instance;
    private final Subject<Object, Object> BUS;

    // PublishSubject只会把在订阅发生的时间点之后来自原始Observable的数据发射给观察者
    public RxBus() {
        BUS = new SerializedSubject<>(PublishSubject.create());
    }

    // 单例RxBus
    public static RxBus getDefault() {
        if (instance == null) {
            synchronized (RxBus.class) {
                if (instance == null) {
                    instance = new RxBus();
                }
            }
        }
        return instance;
    }

    // 发送一个新的事件
    public void post(Object o) {
        BUS.onNext(o);
    }

    // 根据传递的 eventType 类型返回特定类型(eventType)的 被观察者
    public <T> Observable<T> toObservable(Class<T> eventType) {
        return BUS.ofType(eventType);
//        这里感谢小鄧子的提醒: ofType = filter + cast
//        return bus.filter(new Func1<Object, Boolean>() {
//            @Override
//            public Boolean call(Object o) {
//                return eventType.isInstance(o);
//            }
//        }) .cast(eventType);
    }
}
```
#### 使用
```java
  RxBus.getDefault().toObservable(String.class).subscribe(new Action1<String>() {
            @Override
            public void call(String s) {
                Toast.makeText(BleActivity.this,s,Toast.LENGTH_SHORT).show();
            }
        });
```
#### 注意取消订阅
* CompositeSubscription 可以把 Subscription 收集到一起，方便 Activity 销毁时取消订阅，防止内存泄漏。
```java
private CompositeSubscription allSubscription = new CompositeSubscription();
//添加订阅到列表  
allSubscription.add(RxBus.getDefault()
                .toObserverable(OneEvent.class).subscribe(this::response));
//销毁时删除订阅                
@Override
protected void onDestroy() {
        super.onDestroy();
        if (allSubscription != null && !allSubscription.isUnsubscribed())
            allSubscription.unsubscribe();
}
```
