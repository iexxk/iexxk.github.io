---
title: Retrofit学习之三离线缓存
date: 2016-08-26 14:25:44
updated: 2018-12-12 10:47:58categories: Retrofit
tags: [网络框架,Retrofit,缓存]
---
## 创建拦截器（Interceptor）
可以分开写两个拦截器一个有网的一个离线的，这里只写了一个
```java
        //创建拦截器（Interceptor）
        Interceptor REWRITE_CACHE_CONTROL_INTERCEPTOR = new Interceptor() {
            @Override
            public okhttp3.Response intercept(Chain chain) throws IOException {
                okhttp3.Response originalResponse = chain.proceed(chain.request());
                if (com.xuan.bledemo.util.Utils.isNetworkAvailable(MainActivity.this)) {   //判断是否有网络判断
                    int maxAge = 60; //在线缓存在一分钟内读取
                    Log.i("缓存测试", "在线");
                    return originalResponse.newBuilder()
                            .removeHeader("Pragma")   //作用未知
                            .header("Cache-Control", "public,max-age=" + maxAge)
                            .build();
                } else {
                    int maxStale = 60 * 60 * 24 * 28; //离线时缓存保存4周
                    Log.i("缓存测试", "离线");
                    return originalResponse.newBuilder()
                            .removeHeader("Pragma")
                            .header("Cache-Control", "public, only-if-cached, max-stale=" + maxStale)
                            .build();
                }
            }
        };
```

## 设置缓存文件
问题？关于缓存文件在手机上的地方，目前未找到
```java
  //设置缓存文件
  File cacheFile=new File(this.getCacheDir(),"xuanCache");
  Log.i("缓存测试","缓存目录"+this.getCacheDir().getPath());
  Cache cache=new Cache(cacheFile,1024*1024*100); //100mb
```

## 创建httpclient

```java
 //创建httpclient
    OkHttpClient okHttpClient=new OkHttpClient.Builder()
		.cache(cache)
		.addNetworkInterceptor(REWRITE_CACHE_CONTROL_INTERCEPTOR) //添加有网过滤器
		.addInterceptor(REWRITE_CACHE_CONTROL_INTERCEPTOR) //添加无网络过滤器，可以分别定义
		.retryOnConnectionFailure(true)  //出现错误时重新连接
		.connectTimeout(5, TimeUnit.SECONDS) //设置超时时间
		.build();
```

## 将httpclient添加到retrofit
```java
//将http client添加到retrofit
    Retrofit retrofit=new Retrofit.Builder()
    .addConverterFactory(GsonConverterFactory.create())  //添加gson包
    .client(okHttpClient)  //添加自定义的httpclient
    .baseUrl("http://api.zdoz.net/") //添加网址头,注意‘/’结尾
    .build();
```

## 请求数据
第一次必须有网络，后面无网络就是请求缓存
>* enqueue 异步
```java
       Itest itest=retrofit.create(Itest.class); //接口
        Call<Test> getCall= itest.getTest(108.2345);   //传接口参数
        //异步网络请求json数据
        getCall.enqueue(new Callback<Test>() {
           @Override
           public void onResponse(Call<Test> call, Response<Test> response) {
               Log.e("缓存测试","请求成功"+response.body().getD());
           }
           @Override
           public void onFailure(Call<Test> call, Throwable t) {
               Log.e("缓存测试","请求失败"+t.toString());

           }
       });
```

## 问题，未验证
>* 相当与数据库的 POST(创建)、PUT(更新)、GET(查看)、DELETE(删除)
>* 缓存根据查找的资料，好像只有GET可以缓存

## 总结
>* 上述缓存，是同一缓存的配置，如果要单个请求配置，可以设置接口的head,在里面传参数，然后在统一的缓存配置中用参数动态变化没次的不同缓存策略及时间。