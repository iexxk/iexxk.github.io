---
title: greenDAO3.1框架（二）入门
date: 2016-08-27 10:33:45
updated: 2018-04-25 20:41:28categories: greenDAO
tags: [greenDAO,ORM]
---
# 主流的ORM框架
>* LitePal
>* AFinal
>* greenDAO
[区别与性能分析](http://www.jianshu.com/p/8287873d97cd)

# greenDAO3.1 安装
### 配置build.gradle
在model的build.gradle文件添加如下配置
```
buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath 'org.greenrobot:greendao-gradle-plugin:3.1.0'
    }
}

apply plugin: 'org.greenrobot.greendao'

dependencies {
    compile 'org.greenrobot:greendao:3.1.0'
}
```
### 数据库的设置（可选项）
在model的build.gradle文件添加如下配置
```
android {
...
}
 
greendao {
    schemaVersion 2
	...
}
```
参数解释
>* schemaVersion： 数据库schema版本，也可以理解为数据库版本号（默认1）
>* daoPackage：设置DaoMaster 、DaoSession、Dao包名（默认为你实体的名字）
>* targetGenDir：设置DaoMaster 、DaoSession、Dao目录(默认build/generated/source/greendao)
>* testsGenSrcDir：设置生成单元测试目录（默认src/androidTest/java）
>* generateTests：设置自动生成单元测试用例

### 新建实体
添加注解@
```java
@Entity
public class test {
    @Id(autoincrement = true)
    private long tes;

    public long getTes() {
        return tes;
    }

    public void setTes(long tes) {
        this.tes = tes;
    }
}
```
### 编译运行

>* targetGenDir目录(默认build/generated/source/greendao)下自动生成自动生成DaoMaster.java 、DaoSession.java、Dao.java

>* 实体test.java自动新增如下代码

```java
@Generated(hash = 838475940)
    public test(long tes) {
        this.tes = tes;
    }

    @Generated(hash = 1102163179)
    public test() {
    }
```
### 简单的使用
#### 新建DBManager.java管理类
```java
public class DBManager {
    private final static String dbName = "test_db";
    private static DBManager mInstance;
    private DaoMaster.DevOpenHelper openHelper;
    private Context context;

    public DBManager(Context context) {
        this.context = context;
        openHelper = new DaoMaster.DevOpenHelper(context, dbName, null);
    }
    /**
     * 获取单例引用
     *
     * @param context
     * @return
     */
    public static DBManager getInstance(Context context) {
        if (mInstance == null) {
            synchronized (DBManager.class) {
                if (mInstance == null) {
                    mInstance = new DBManager(context);
                }
            }
        }
        return mInstance;
    }

    /**
     * 获取可读数据库
     */
    private SQLiteDatabase getReadableDatabase() {
        if (openHelper == null) {
            openHelper = new DaoMaster.DevOpenHelper(context, dbName, null);
        }
        SQLiteDatabase db = openHelper.getReadableDatabase();
        return db;
    }
    /**
     * 获取可写数据库
     */
    private SQLiteDatabase getWritableDatabase() {
        if (openHelper == null) {
            openHelper = new DaoMaster.DevOpenHelper(context, dbName, null);
        }
        SQLiteDatabase db = openHelper.getWritableDatabase();
        return db;
    }
    /**
     * 插入一条记录
     *
     * @param test
     */
    public void insertUser(test test) {
        DaoMaster daoMaster = new DaoMaster(getWritableDatabase());
        DaoSession daoSession = daoMaster.newSession();
        testDao userDao = daoSession.getTestDao();
        userDao.insert(test);
    }
    /**
     * 查询用户列表
     */
    public List<test> queryUserList() {
        DaoMaster daoMaster = new DaoMaster(getReadableDatabase());
        DaoSession daoSession = daoMaster.newSession();
        testDao userDao = daoSession.getTestDao();
        QueryBuilder<test> qb = userDao.queryBuilder();
        List<test> list = qb.list();
        return list;
    }
}
```
#### 测试代码
```java
private void daotest(){
    DBManager dbManager=DBManager.getInstance(this);
    dbManager.insertUser(new test(10));
    Log.i("sssss","ddddd"+dbManager.queryUserList().get(0).getTes());
}
```
# 参考
[Android数据存储之GreenDao 3.0 详解](http://www.tuicool.com/articles/63I3EfB)
[官方教程](http://greenrobot.org/greendao/documentation/updating-to-greendao-3-and-annotations/)



