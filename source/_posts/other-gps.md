---
title: Gps认识之各大坐标系
date: 2016-08-23 16:03:33
updated: 2018-12-12 10:47:58
categories: 杂谈
tags: [gps,location,火星,地球,坐标]
---
# 三大定位坐标系

## 地球坐标 (WGS84)
>* 国际标准，从 GPS 设备中取出的数据的坐标系
>* 国际地图提供商使用的坐标系

## 火星坐标 (GCJ-02)也叫国测局坐标系
>* 中国标准，从国行移动设备中定位获取的坐标数据使用这个坐标系
>* 国家规定： 国内出版的各种地图系统（包括电子形式），必须至少采用GCJ-02对地理位置进行首次加密。

## 百度坐标 (BD-09)
>* 百度标准，百度 SDK，百度地图，Geocoding 使用
>* (本来就乱了，百度又在火星坐标上来个二次加密)

# 现在说说各大地图图层及定位的坐标系
图层坐标是指地图的坐标，不是实际的gps坐标，中国规定：中国区域必须对图层加密，所以实际坐标并不是真实的gps坐标（WGS84）
,是加密过后的火星坐标（GCJ-02）或者火星坐标（BD-09）.

## 图层坐标系
>* 百度地图 （BD-09）
>* 谷歌地图 （国内GCJ-02,国外WGS84）
>* 谷歌地球 （国内国外WGS84）
>* 高德地图 （GCJ-02)

## 定位坐标系
>* 百度地图sdk (BD-09)
>* 谷歌地图sdk (WGS84)
>* 高德地图sdk (GCJ-02)
>* android原生定位sdk (WGS84)

# 高德地图api

## 坐标转换与位置判断
>* 坐标转换
>  支持GPS/Mapbar/Baidu等多种类型坐标在高德地图上使用。参见类CoordinateConverter。
```java
CoordinateConverter converter  = new CoordinateConverter(); 
// CoordType.GPS 待转换坐标类型
converter.from(CoordType.GPS); 
// sourceLatLng待转换坐标点 DPoint类型
converter.coord(sourceLatLng); 
// 执行转换操作
DPoint desLatLng = converter.convert();
```
>* 判断位置所在区域
```java
CoordinateConverter类提供的isAMapDataAvailable(double latitude,double longitude)接口可以用来判断指定位置是否在大陆以及港、澳地区。
CoordinateConverter converter  = new CoordinateConverter(); 
//返回true代表当前位置在大陆、港澳地区，反之不在。
boolean isAMapDataAvailable = converter.isAMapDataAvailable(latitude,longitude);
//第一个参数为纬度，第二个为经度，纬度和经度均为高德坐标系。
```

# 总结：
如果用高德和google双地图，可以采用高德的坐标转换工具判断及转换给google，因为google和高德图层都是火星坐标