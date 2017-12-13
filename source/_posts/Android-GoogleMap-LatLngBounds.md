---
title: GooleMap之自动缩放以显示所有标记
date: 2016-09-02 10:45:56
categories: Android
tags: [GoogleMap,LatLngBounds]
---
## [官方描述](https://developers.google.com/maps/documentation/android-api/views?hl=zh-cn)
### 设置边界
有时，通过移动摄像头来以尽可能最高的缩放级别显示整个受关注区域很有用处。 例如， 如果您要显示用户当前位置方圆五英里内的所有加油站， 可能就需要通过移动摄像头让它们全都显示在屏幕上。 如需实现此目的，请先计算您想在屏幕上显示的 LatLngBounds。 然后使用 CameraUpdateFactory.newLatLngBounds(LatLngBounds bounds, int padding) 获取 CameraUpdate，后者会相应更改摄像头位置，使得给定 LatLngBounds 在计入所指定内边距（单位：像素）后能够完全容纳在地图内。 返回的 CameraUpdate 可确保给定边界与地图边缘之间的间隙（单位：像素）至少与指定的内边距一样大。 请注意，地图的倾斜角度和方位均为 0。
```java
private GoogleMap mMap;
// Create a LatLngBounds that includes Australia.
private LatLngBounds AUSTRALIA = new LatLngBounds(
  new LatLng(-44, 113), new LatLng(-10, 154));

// Set the camera to the greatest possible zoom level that includes the
// bounds
mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(AUSTRALIA, 0));
```
### [LatLngBounds](https://developers.google.com/android/reference/com/google/android/gms/maps/model/LatLngBounds?hl=zh-cn)

>* public LatLngBounds including (LatLng point)   包含显示的点
>* public LatLng getCenter ()  获得中心点

### 代码的具体实现
```java
 LatLngBounds.Builder latLngBounds=new LatLngBounds.Builder();
   for (int i=0;i<latLngs.size();i++){
       latLngBounds.include(latLngs.get(i));
   }
   googleMap.moveCamera(CameraUpdateFactory.newLatLngBounds(latLngBounds.build(), 30));
```
### 问题
如果直接在获取到地图后调用会报错
解决：在回调里调用
```java 
googleMap.setOnMapLoadedCallback(this); 
 @Override
    public void onMapLoaded() {
	//添加实现的代码
	}
```
