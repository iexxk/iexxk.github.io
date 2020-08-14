---
title: Android-osmdroid-kml
date: 2018-12-28 17:58:01
updated: 2018-12-28 18:05:04
categories: Android
tags: [osmdroid]
---

## [osmdroid 加载kml/kmz文件](https://github.com/MKergall/osmbonuspack/wiki/Tutorial_4)

1. 首先增加导入`compile 'com.github.MKergall:osmbonuspack:6.5.2'`

2. 添加代码

   ```java
       class KmlLoader extends AsyncTask<Void, Void, Void> {
           ProgressDialog progressDialog = new ProgressDialog(context);
           KmlDocument kmlDocument;
   
           @Override
           protected void onPreExecute() {
               super.onPreExecute();
               progressDialog.setMessage("Loading Project...");
               progressDialog.show();
           }
   
           @Override
           protected Void doInBackground(Void... voids) {
               File f = new File(Environment.getExternalStorageDirectory().getAbsolutePath() + "/osmdroid/"+Config.KMLFILENAME);
               kmlDocument = new KmlDocument();
              	//加载kml文件修改为parseKMLFile
               kmlDocument.parseKMZFile(f);
               FolderOverlay kmlOverlay = (FolderOverlay)kmlDocument.mKmlRoot.buildOverlay(mapView, null, null,kmlDocument);
               mapView.getOverlays().add(kmlOverlay);
               return null;
           }
   
           @Override
           protected void onPostExecute(Void aVoid) {
               progressDialog.dismiss();
               mapView.invalidate();
               BoundingBox bb = kmlDocument.mKmlRoot.getBoundingBox();
               mapView.zoomToBoundingBox(bb, true);
   //            mapView.getController().setCenter(bb.getCenter());
               super.onPostExecute(aVoid);
           }
       }
   ```

3. 引用代码`new KmlLoader().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);`

#### shp  kml kmz文件转换可以用Google earth桌面软件

或者[Tools-geoserver-base](http://blog.iexxk.com/2018/08/17/Tools-geoserver-base/)

