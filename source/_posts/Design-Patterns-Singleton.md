---
title: 设计模式之单例模式
date: 2016-09-30 12:40:27
updated: 2018-01-28 21:41:27categories: 设计模式
tags: [单例,设计模式,框架]
---

### 懒汉式
* 使用时才实例化
* 使用场景：单例使用次数不多、功能复杂，占用内存大、实例化时间长、特定场景、延迟加载。
*  ==线程不安全==：多个线程可能会并发调用他的newInstance方法导致多个线程可能会创建多份相同的单例出来。
```java
public class Singleton{
    private static Singleton instance = null;

    private Singleton(){}

    public static Singleton newInstance(){
        if(null == instance){
            instance = new Singleton();
        }
        return instance;
    }
}
```

### 懒汉式同步锁
使用同步锁`synchronized (Singleton.class)`解决线程不安全问题
```java
public class Singleton {
 
    private static Singleton instance = null;
 
    private Singleton(){
    }
 
    public static Singleton getInstance() {
        synchronized (Singleton.class) {
            if (instance == null) {
                instance = new Singleton();
            }
        }
 
        return instance;
    }
}
```
### 双重校验锁
```java
public class Singleton {
 
    private static volatile Singleton instance = null;
 
    private Singleton(){
    }
 
    public static Singleton getInstance() {
        // if already inited, no need to get lock everytime
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
 
        return instance;
    }
}
```

### 饿汉式
* 简单快速，实例化快
* 使用场景：占用内存较小的、应用启动时加载初始化的
* 线程安全：因为JVM只会加载一次单例类
```java
public class Singleton{

    private static Singleton instance = new Singleton();

    private Singleton(){}

    public static Singleton newInstance(){
        return instance;
    }
}
```

## jvm的类加载机制
JVM已经为我们提供了同步控制
>* 在static{}区块中初始化的数据
>* 访问final字段时
>* .....

### 静态内部类
* 简洁
* 使用场景：
* 线程安全：
```java
public class Singleton{
    //内部类，在装载该内部类时才会去创建单利对象
    private static class SingletonHolder{
        public static Singleton instance = new Singleton();
    }

    private Singleton(){}

    public static Singleton newInstance(){
        return SingletonHolder.instance;
    }

    public void doSomething(){
        //do something
    }
}
```
### 枚举类
* 最简单
* 线程安全：
```java
public enum Singleton{
    //定义一个枚举的元素，它就是Singleton的一个实例
    instance;

    public void doSomething(){
        // do something ...
    }    
}
```

### 使用方法
```java
public static void main(String[] args){
   Singleton singleton = Singleton.instance;
   singleton.doSomething();
}
```
### 参考
[ANDROID设计模式之单例模式](http://stormzhang.com/designpattern/2016/03/27/android-design-pattern-singleton/)