---
title: android自定义标题栏Toolbar
date: 2016-08-30 16:17:33
categories: Android
tags: [v7,标题栏]
---
### 新建一个xml,放标题内容
```xml
<?xml version="1.0" encoding="utf-8"?>
    <android.support.v7.widget.Toolbar xmlns:android="http://schemas.android.com/apk/res/android"
        android:id="@+id/toolbar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@color/colorPrimary">
        <!--自定义控件-->
        <!--<TextView-->
            <!--android:layout_width="wrap_content"-->
            <!--android:layout_height="wrap_content"-->
            <!--android:text="标题" />-->
    </android.support.v7.widget.Toolbar>
```
### 在需要的页面调用
```xml
 <include
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        layout="@layout/activity_tool_bar" />
```
### 去掉自带标题
在配置文件找到
```xml
 android:theme="@style/AppTheme"
```
点击进去把parent修改为NoActionBar
```xml
  <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Customize your theme here. -->
        <!--最顶层的颜色消息时间栏-->
        <item name="colorPrimary">@color/colorPrimary</item>
        <!--标题栏颜色-->
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <!--应用内系统控件的颜色，例如系统的滑动条等-->
        <item name="colorAccent">@color/colorAccent</item>
    </style>
```
### 在activity里获取标题控件,设置基本属性
```java
 toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("标题"); 
        toolbar.setSubtitle("副标题");
        toolbar.setTitleTextColor(Color.WHITE); //颜色
        toolbar.setSubtitleTextColor(Color.WHITE);
        toolbar.setLogo(R.mipmap.debug); //图标

        //设置导航图标要在setSupportActionBar方法之后
        setSupportActionBar(toolbar);
        toolbar.setNavigationIcon(R.mipmap.ic_launcher);
```
### 在activity添加标题栏返回箭头
使能返回button
```java
toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("标题");
        toolbar.setSubtitle(副标题);
        //设置导航图标要在setSupportActionBar方法之后
        setSupportActionBar(toolbar);
        if(getSupportActionBar() != null)
        getSupportActionBar().setDisplayHomeAsUpEnabled(true); // Enable the Up button
```
添加返回button事件
```java
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case android.R.id.home: //返回键
			//添加处理代码
              break;
        }
        return super.onOptionsItemSelected(item);
    }
```