---
title: Retrofit学习之二请求json
date: 2016-08-25 12:52:21
updated: 2016-08-26 14:25:13categories: Retrofit
tags: [网络框架,Retrofit]
---
# 创建json对应得实体类
测试网址：[http://api.zdoz.net/DDD2DMS.aspx?gps=108.2345](http://api.zdoz.net/DDD2DMS.aspx?gps=108.2345)
>* 新建一个实体类Test.java，把json数据通过gsonFormat插件生成对应得属性方法

# 创建接口

>* 新建一个接口类Itest.java
```java
public interface Itest {
    @GET("DDD2DMS.aspx")
    Call<Test> getTest(@Query("gps") double gps);
}
```
# 请求json数据
```java
  Retrofit retrofit=new Retrofit.Builder()
				//如果是json数据必须加这句
                .addConverterFactory(GsonConverterFactory.create())  
                .baseUrl("http://api.zdoz.net/")
				.build();
        Itest itest=retrofit.create(Itest.class);
        Call<Test> testCall= itest.getTest(108.2345);
        testCall.enqueue(new Callback<Test>() {
           @Override
           public void onResponse(Call<Test> call, Response<Test> response) {
               Log.e("得到得json数据",""+response.body().getD());
           }
           @Override
           public void onFailure(Call<Test> call, Throwable t) {

           }
       });
```
### 参数详解
>* enqueue 异步请求
>* execute 同步请求
>* baseUrl参数以'/'结束

