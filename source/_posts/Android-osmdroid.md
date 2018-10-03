---
title: Android-osmdroid
date: 2018-05-29 15:59:44
updated: 2018-09-28 20:42:55
categories: Android
tags: [osmdroid]
---

#### 参考工具

github: [osmdroid/osmdroid](https://github.com/osmdroid/osmdroid)

`compile 'org.osmdroid:osmdroid-android:<VERSION>'`

离线地图制作工具: [Mobile Atlas Creator](http://mobac.sourceforge.net/)

[使用Mobile Atlas Creator](https://mobiledevstories.wordpress.com/2014/02/27/osmdroid-mobile-atlas-creator-tutorial/)

[wiki map sources](https://github.com/osmdroid/osmdroid/wiki/Map-Sources)

离线地图工具类[SampleOfflineOnly.java](https://github.com/osmdroid/osmdroid/blob/master/OpenStreetMapViewer/src/main/java/org/osmdroid/samplefragments/tileproviders/SampleOfflineOnly.java)

[离线地图官方教程Offline-Map-Tiles](https://github.com/osmdroid/osmdroid/wiki/Offline-Map-Tiles)

### 操作步骤

##### 离线地图制作

1. 打开[Mobile Atlas Creator](http://mobac.sourceforge.net/)工具
2. 新建地图册（可选Osmdroid ZIP/SQLite/GEMF）
3. 选择地图源
4. 勾选图片转换，设置图块格式(**重要，要和代码的设置一致**)
5. 设置缩放比例
6. 地图上框选区域
7. 在当前地图册点击添加选择区域
8. 最后开始点击下载地图册
9. 得到一个压缩文件，存储备用

##### 离线地图自定义地图源(geoserver)

1. 在[Mobile Atlas Creator](http://mobac.sourceforge.net/)工具目录的`mapsources`目录添加地图源配置文件

2. geoserver地图地图源配置文件`geoserver_maps.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
     <customWmsMapSource>
     <name>My Geoserver WMS</name>
     <minZoom>0</minZoom>
     <maxZoom>18</maxZoom>
     <tileType>PNG</tileType>
     <version>1.1.1</version>
       <!-- 图层名字hws(工作空间):china_net(图层名字) -->
     <layers>hws:china_net</layers>
      <!-- hws替换为自己的工作区间，ip端口替换自己服务器的，其他不变 -->
     <url>http://192.168.1.230:8082/geoserver/hws/wms?service=WMS&amp;</url>
      <!-- 投影坐标系 -->
     <coordinatesystem>EPSG:4326</coordinatesystem>
     <aditionalparameters></aditionalparameters>
     <backgroundColor>#000000</backgroundColor>
   </customWmsMapSource>
   ```

3. 多图层配置

   ```xml
   <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
   <customMultiLayerMapSource>
      <name>geoserver ygl ch</name>
      <tileType>png</tileType>
      <backgroundColor>#000000</backgroundColor>
      <!-- 从底部（第一个）到顶部（最后一个）的每个图层的不透明度值列表。值0.0完全透明或不可见，而值1.0完全不透明。通常第一层应使用1.0 = 100％不透明度 -->
      <layersAlpha>1.0 0.5</layersAlpha>
      <layers>
   		 <customWmsMapSource>
   		  <name>ch</name>
   		  <minZoom>0</minZoom>
   		  <maxZoom>18</maxZoom>
   		  <tileType>PNG</tileType>
   		  <version>1.1.1</version>
   			<!-- 图层名字hws(工作空间):china_net(图层名字) -->
   		  <layers>hws:china_net</layers>
   		   <!-- hws替换为自己的工作区间，ip端口替换自己服务器的，其他不变 -->
   		  <url>http://192.168.1.230:8082/geoserver/hws/wms?service=WMS&amp;</url>
   		   <!-- 投影坐标系 -->
   		  <coordinatesystem>EPSG:4326</coordinatesystem>
   		  <aditionalparameters></aditionalparameters>
   		  <!-- <backgroundColor>#000000</backgroundColor> -->
   		</customWmsMapSource>
   		<customWmsMapSource>
   		  <name>ygl</name>
   		  <minZoom>0</minZoom>
   		  <maxZoom>18</maxZoom>
   		  <tileType>PNG</tileType>
   		  <version>1.1.1</version>
   			<!-- 图层名字hws(工作空间):china_net(图层名字) -->
   		  <layers>hws:yinggeling18</layers>
   		   <!-- hws替换为自己的工作区间，ip端口替换自己服务器的，其他不变 -->
   		  <url>http://192.168.1.230:8082/geoserver/hws/wms?service=WMS&amp;</url>
   		   <!-- 投影坐标系 -->
   		  <coordinatesystem>EPSG:4326</coordinatesystem>
   		  <aditionalparameters></aditionalparameters>
   		  <!-- <backgroundColor>#000000</backgroundColor> -->
   		</customWmsMapSource>
      </layers>
   </customMultiLayerMapSource>
   ```

##### 离线地图自定义地图源(google地图)

1. 在[Mobile Atlas Creator](http://mobac.sourceforge.net/)工具目录的`mapsources`目录添加地图源配置文件

2. google地图地图源配置文件`google_maps.xml`

   ```xml
   <?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
   <customMultiLayerMapSource> 
       <name>Google 卫星</name> 
       <tileType>PNG</tileType> 
       <layers> 
           <customMapSource> 
               <name>Google 卫星图</name> 
               <minZoom>0</minZoom> 
               <maxZoom>20</maxZoom> 
               <tileType>PNG</tileType> 
               <tileUpdate>None</tileUpdate> 
               <url>http://mt0.google.cn/vt/lyrs=s@124&amp;hl=zh-CN&amp;gl=CN&amp;src=app&amp;x={$x}&amp;s=&amp;y={$y}&amp;z={$z}&amp;s=Galileo</url> 
               <backgroundColor>#000000</backgroundColor> 
           </customMapSource> 
           <customMapSource> 
               <name>Google 地名图</name> 
               <minZoom>0</minZoom> 
               <maxZoom>20</maxZoom> 
               <tileType>PNG</tileType> 
               <tileUpdate>None</tileUpdate> 
               <url>http://mt0.google.cn/vt/imgtp=png32&amp;lyrs=h@207000000&amp;hl=zh-CN&amp;gl=CN&amp;src=app&amp;x={$x}&amp;y={$y}&amp;z={$z}&amp;s=Galil</url> 
           </customMapSource> 
       </layers> 
   </customMultiLayerMapSource>
   ```

3. 地图源文件xml的设置搜索`Mobile Atlas Creator自定义地图源`

   [IPad 離線地圖：「Mobile Atlas Creator + 地圖加加」，讓google map成為好用的離線地圖!!](https://doc-pi.blogspot.com/2015/07/ipad-mobile-atlas-creator-google-map.html)

#### Android代码设置

1. 导包``compile 'org.osmdroid:osmdroid-android:<VERSION>'``

2. 手动设置离线地图的文件

   ```java
   //路径压缩包的路径放在存储目录下/osmdroid/Google Maps（世界墨卡托）.zip这个是刚刚用工具制作得到的压缩文件
   String path=Environment.getExternalStorageDirectory().getAbsolutePath() + "/osmdroid/"+"Google Maps（世界墨卡托）.zip";
   //设置为离线工作模式。路径一定要对，而且只支持 ZIP/SQLite/GEMF
   mapView.setTileProvider(new OfflineTileProvider(new SimpleRegisterReceiver(this),new File[]{new File(path)}));
   //这里Google Map为压缩文件的第一层目录名，一定要一致，.png.tile为最内层目录的文件后缀名一点定要一致，一般是png，这里比较特殊
   mapView.setTileSource(new XYTileSource("Google Map", 7, 16,
                   256, ".png.tile", null));
   ```

3. 上面那步基本就可以解析了，官方使用[SampleOfflineOnly.java](https://github.com/osmdroid/osmdroid/blob/master/OpenStreetMapViewer/src/main/java/org/osmdroid/samplefragments/tileproviders/SampleOfflineOnly.java)做自动解析

   ```java
   //设置离线地图的路径
   File f = new File(Environment.getExternalStorageDirectory().getAbsolutePath() + "/osmdroid/");
   if (f.exists()) {  //判断目录是否存在
       File[] list = f.listFiles(); //得到该目录下的文件
       if (list != null) {
           for (int i = 0; i < list.length; i++) {  //遍历的得到的所有目录和文件
               if (list[i].isDirectory()) {  //目录跳过
                   continue;
               }
               String name = list[i].getName().toLowerCase();
               if (!name.contains(".")) {  //没有后缀跳过
                   continue; //skip files without an extension
               }
               name = name.substring(name.lastIndexOf(".") + 1);  //得到后缀名
               if (name.length() == 0) {
                   continue;
               }
               if (ArchiveFileFactory.isFileExtensionRegistered(name)) { //后缀名是否是ZIP/SQLite/GEMF其中一个
                   try {
                       OfflineTileProvider tileProvider = new OfflineTileProvider(new SimpleRegisterReceiver(this),
                                                                                  new File[]{list[i]});  //如果是把该文件作为离线地图的提供者
                       mapView.setTileProvider(tileProvider);  // <重要>
                       String source = "";
                       IArchiveFile[] archives = tileProvider.getArchives();
                       if (archives.length > 0) {
                           Set<String> tileSources = archives[0].getTileSources();
                           if (!tileSources.isEmpty()) {
                               source = tileSources.iterator().next();  //活动压缩文件第一级目录的目录名
                               //自定义设置  <重要> ，其中文件后缀名要和压缩文件内的后缀一致
                               this.mapView.setTileSource(new FileBasedTileSource(source,0, 18, 256, ".png", null));
                               //   this.mapView.setTileSource(FileBasedTileSource.getSource(source));  //默认设置
                           } else {
                               this.mapView.setTileSource(TileSourceFactory.DEFAULT_TILE_SOURCE);
                           }
                       } else {
                           this.mapView.setTileSource(TileSourceFactory.DEFAULT_TILE_SOURCE);
                       }
                       this.mapView.invalidate();
                       return;
                   } catch (Exception ex) {
                       ex.printStackTrace();
                   }
               }
           }
       }
       Toast.makeText(this, f.getAbsolutePath() + " did not have any files I can open! Try using MOBAC", Toast.LENGTH_SHORT).show();
   } else {
       Toast.makeText(this, f.getAbsolutePath() + " dir not found!", Toast.LENGTH_SHORT).show();
   }
   ```


##### 参考

[How to use Custom map in MOBAC?](https://gis.stackexchange.com/questions/72898/how-to-use-custom-map-in-mobac)







