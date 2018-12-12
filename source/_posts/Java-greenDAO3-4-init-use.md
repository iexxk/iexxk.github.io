---
title: greenDAO3.1框架（四）添加全局初始化及基本使用
date: 2016-08-31 10:50:45
updated: 2018-01-28 21:41:27categories: greenDAO
tags: [greenDAO,ORM,application,path]
---
### 全局初始化greenDAO设置
```java
public class UserGlobalApp extends Application{
    private static UserGlobalApp application;
    private final static String dbName = "HiJia"; //数据库名字
    /** A flag to show how easily you can switch from standard SQLite to the encrypted SQLCipher. */
    public static final boolean ENCRYPTED = false;  //改为true需要加入包compile 'net.zetetic:android-database-sqlcipher:3.5.1'
    private DaoSession daoSession;
	  @Override
    public void onCreate() {
        super.onCreate();
        application=this;
       initDb();
    }

    /***
     * 初始化greenDao
     * 数据库
     */
    private void initDb(){
    DaoMaster.DevOpenHelper helper = new DaoMaster.DevOpenHelper(this, ENCRYPTED ? dbName+"-encrypted.db" : dbName+".db",null);
    Database db = ENCRYPTED ? helper.getEncryptedWritableDb("super-secret") : helper.getWritableDb();
    daoSession = new DaoMaster(db).newSession();
	}
    public DaoSession getDaoSession() {
        return daoSession;
    }

	public static UserGlobalApp getApplication(){
		return application;
	}
}
```
### 使用
添加数据，查询数据
```java
UserGlobalApp.getApplication().getDaoSession().getTrackPointDao().insert(new TrackPoint((long) 10,System.currentTimeMillis(),10.01,10.02,1));
Log.i("sssss",""+UserGlobalApp.getApplication().getDaoSession().getTrackPointDao().loadAll().size());

```

### 生成的dao目录配置（非必须）
```
//------------greenDAO数据库配置-----------
greendao {
    schemaVersion 1   //数据库版本
    daoPackage'com.xuan.bledemo.db.greendao'  //dao的存放目录
    targetGenDir'src/main/java' 
}

```
# 问题
数据库加密问题
在全局配置中如果要加密，要设置为true，但是设置为ture会报错
```java
 public static final boolean ENCRYPTED = false;  //改为true需要加入包compile 
```
解决：因为没有加密包，需要添加依赖
```
compile 'net.zetetic:android-database-sqlcipher:3.5.1'
```

# 数据库路径设置
```java
 File path=new File(Environment.getExternalStorageDirectory(),"BleDemo/db/"+dbName);  //设置存储路径
 path.getParentFile().mkdirs();
 DaoMaster.DevOpenHelper helper = new DaoMaster.DevOpenHelper(this, ENCRYPTED ? path.getAbsolutePath()+"-encrypted.db" : path.getAbsolutePath()+".db",null);
```



