---
title: RxJava概念(1)
date: 2016-09-08 17:15:44
categories: RxJava
tags: [异步,RxJava,简洁,观察者]
---
### button点击事件
```java
	button.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {

        }
    });
    button.performClick(); //触发点击事件
```
从上面代码理解：
**被观察者**`Observable`----->`button`----->一些操作，事件，任务（相当于我们不知道`button`什么时候被点击）
**观察者**`Observer`/`Subscriber`----->`OnClickListener`----->决定事件触发的时候将有怎样的行为
**订阅**`Subscribe`----->`setOnClickListener`----->注册事件关联
**事件**`onNext()`/`onCompleted()`/`onError()`----->`onClick()`----->回调，最终结果(`Subscriber`多了`onStart()``unsubscribe()`)

### `Observable` **被观察者**
创建被观察者
>* `creat()` 最基本的创造事件序列的方法
```java
Observable observable = Observable.create(new Observable.OnSubscribe<String>() {
    @Override
    public void call(Subscriber<? super String> subscriber) {
        subscriber.onNext("Hello");
        subscriber.onNext("Hi");
        subscriber.onNext("Aloha");
        subscriber.onCompleted();
    }
});
```
>* `just()`  快捷创建事件序列
```java
Observable observable = Observable.just("Hello", "Hi", "Aloha");
// 将会依次调用：
// onNext("Hello");
// onNext("Hi");
// onNext("Aloha");
// onCompleted();
```
>* `from()`  传入的数组或 Iterable 拆分成具体对象后，依次发送出来
```java
String[] words = {"Hello", "Hi", "Aloha"};
Observable observable = Observable.from(words);
// 将会依次调用：
// onNext("Hello");
// onNext("Hi");
// onNext("Aloha");
// onCompleted();
```
>* `ActionX` 自定义(`onCompleted`,`onError`,`onNext`) 无返回值
>* `FuncX` 有返回值
```java
Action1<String> onNextAction = new Action1<String>() {
    // onNext()
    @Override
    public void call(String s) {
        Log.d(tag, s);
    }
};
Action1<Throwable> onErrorAction = new Action1<Throwable>() {
    // onError()
    @Override
    public void call(Throwable throwable) {
        // Error handling
    }
};
Action0 onCompletedAction = new Action0() {
    // onCompleted()
    @Override
    public void call() {
        Log.d(tag, "completed");
    }
};

// 自动创建 Subscriber ，并使用 onNextAction 来定义 onNext()
observable.subscribe(onNextAction);
// 自动创建 Subscriber ，并使用 onNextAction 和 onErrorAction 来定义 onNext() 和 onError()
observable.subscribe(onNextAction, onErrorAction);
// 自动创建 Subscriber ，并使用 onNextAction、 onErrorAction 和 onCompletedAction 来定义 onNext()、 onError() 和 onCompleted()
observable.subscribe(onNextAction, onErrorAction, onCompletedAction);
```
### `Scheduler` 线程控制(调度器)
>* `Schedulers.immediate()`:直接在当前线程运行，相当于不指定线程。这是默认的 `Scheduler`。
>* `Schedulers.newThread()`:总是启用新线程，并在新线程执行操作。
>* `Schedulers.io()`: I/O 操作（读写文件、读写数据库、网络信息交互等）所使用的 Scheduler。行为模式和 newThread() 差不多，区别在于 io() 的内部实现是是用一个无数量上限的线程池，可以重用空闲的线程，因此多数情况下 io() 比 newThread() 更有效率。不要把计算工作放在 io() 中，可以避免创建不必要的线程。
>* `Schedulers.computation()`:计算所使用的 Scheduler。这个计算指的是 CPU 密集型计算，即不会被 I/O 等操作限制性能的操作，例如图形的计算。这个 Scheduler 使用的固定的线程池，大小为 CPU 核数。不要把 I/O 操作放在 computation() 中，否则 I/O 操作的等待时间会浪费 CPU。
>* `AndroidSchedulers.mainThread()`:指定的操作将在 Android 主线程运行。
```java
Observable.just(1, 2, 3, 4)
    .subscribeOn(Schedulers.io()) // 指定 subscribe() 发生在 IO 线程
    .observeOn(AndroidSchedulers.mainThread()) // 指定 Subscriber 的回调发生在主线程
    .subscribe(new Action1<Integer>() {
        @Override
        public void call(Integer number) {
            Log.d(tag, "number:" + number);
        }
    });
```
### 变换
>* `map()`
>* `flatMap()`