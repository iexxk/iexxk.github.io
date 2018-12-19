---
title: DB-Realm-Base
date: 2018-05-26 15:35:08
updated: 2018-12-12 10:47:58
categories: 数据库
tags: [数据库,android]
---

## 简介

[官网](https://realm.io/docs/java/latest/)

全平台通用数据库

1. 特点自带通知
2. 实体类方式

### 使用

1. 在project中的build.gradle添加

   ```groovy
       dependencies {
           classpath "io.realm:realm-gradle-plugin:5.1.0"
       }
   ```

2. 在model中的build.gradle添加

   ```groovy
   apply plugin: 'realm-android'
   ```

3. 新建实体类，两种方式

   方式一

   ```java
   @RealmClass
   public class TestEntiy implements RealmModel {
       private Long id;
       ......
   }
   ```

   方式二

   ```java
   public class TestEntiy extends RealmModel {
       private Long id;
       ......
   }
   ```

4. 在application中初始化realm

   ```java
   Realm.init(context); //数据库初始化
   RealmConfiguration config = new RealmConfiguration.Builder().name("mulun.realm").build();
   Realm.setDefaultConfiguration(config);  //设置配置，数据库文件名为mulun.realm
   //测试
   Realm realm = Realm.getDefaultInstance(); //获取数据库实例
   Log.i("MyApplication","数据库路径为："+realm.getPath()); //打印路径
   realm.close(); //用完需要关闭实例
   ```

5. 在data/data/包名/file目录下可以找到数据库文件`mulun.realm`

6. 该文件可以通过`Realm Studio`打开

### 进阶

数据库插入/删除数据

```java
Realm realm = Realm.getDefaultInstance(); //获取数据库实例
//方式一
TestEntiy testEntiy=new TestEntiy();        
realm.executeTransaction(new Realm.Transaction() {
    @Override
    public void execute(Realm realm) {
        realm.copyToRealm(testEntiy);
    }
});
//查询删除数据，该查询是异步的，如果数据testEntiy发生了修改和增加会在这里收到通知
realm.where(TestEntiy.class).findAllAsync().asFlowable().subscribe(new Consumer<RealmResults<TestEntiy>>() {
    @Override
    public void accept(final RealmResults<TestEntiy> testEntiy) throws Exception {
         TestEntiy testEntiyRes = realm.copyFromRealm(testEntiy); //此种方式才能真正取到实体类，不能直接用testEntiy
        realm.executeTransaction(new Realm.Transaction() {
            @Override
            public void execute(Realm realm) {
                testEntiy.deleteAllFromRealm();   //上传失败删除数据
            }
        });
    }
}
                                                                   realm.close();
```

另一种操作方式

```java
Realm realm = Realm.getDefaultInstance(); //获取数据库实例
realm.beginTransaction();
realm.copyToRealm(testEntiy);
realm.commitTransaction();
realm.close();
```











